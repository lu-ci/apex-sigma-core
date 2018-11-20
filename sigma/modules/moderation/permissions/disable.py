# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied
from sigma.modules.moderation.permissions.nodes.permission_data import get_all_perms


async def disable(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            if ':' in pld.args[0]:
                perm_mode = pld.args[0].split(':')[0].lower()
                node_name = pld.args[0].split(':')[1].lower()
                modes = {
                    'c': ('Command', 'disabled_commands', cmd.bot.modules.commands, True),
                    'm': ('Module', 'disabled_modules', cmd.bot.modules.categories, False)
                }
                mode_vars = modes.get(perm_mode.lower())
                if mode_vars:
                    mode_name, exception_group, check_group, check_alts = mode_vars
                    if check_alts:
                        if node_name in cmd.bot.modules.alts:
                            node_name = cmd.bot.modules.alts[node_name]
                    if node_name in check_group:
                        perms = await get_all_perms(cmd.db, pld.msg)
                        disabled_items = perms[exception_group]
                        if node_name not in disabled_items:
                            disabled_items.append(node_name)
                            perms.update({exception_group: disabled_items})
                            await cmd.db[cmd.db.db_nam].Permissions.update_one(
                                {'server_id': pld.msg.guild.id}, {'$set': perms})
                            await cmd.db.cache.del_cache(pld.msg.guild.id)
                            response = discord.Embed(color=0x77B255, title=f'✅ `{node_name.upper()}` disabled.')
                        else:
                            response = discord.Embed(color=0xFFCC4D, title=f'⚠ {mode_name} already disabled.')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 {mode_name} not found.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Unrecognized lookup mode, see usage example.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Separate permission type and name with a colon.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)
