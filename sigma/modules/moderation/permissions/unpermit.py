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
from sigma.core.utilities.generic_responses import permission_denied
from sigma.modules.moderation.permissions.permit import get_perm_group, get_targets, get_target_type


def verify_targets(targets: list, exc_tuple: tuple, exc_group: str, node_name: str, target_type: str, perms: dict):
    exc_usrs, inner_exc, cmd_exc = exc_tuple
    bad_item = False
    for target in targets:
        if target.id in exc_usrs:
            exc_usrs.remove(target.id)
            inner_exc.update({target_type: exc_usrs})
            cmd_exc.update({node_name: inner_exc})
            perms.update({exc_group: cmd_exc})
        else:
            bad_item = target
            break
    return bad_item


async def unpermit(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 3:
                if ':' in args[1]:
                    target_type = get_target_type(args[0].lower())
                    if target_type:
                        perm_mode = args[1].split(':')[0]
                        node_name = args[1].split(':')[1]
                        modes = {
                            'c': ('command_exceptions', cmd.bot.modules.commands, True),
                            'm': ('module_exceptions', cmd.bot.modules.categories, False)
                        }
                        mode_vars = modes.get(perm_mode)
                        if mode_vars:
                            exc_group, check_group, check_alts = mode_vars
                            targets, valid_targets = get_targets(message, args, target_type)
                            if valid_targets:
                                exc_tuple, node_name, perms = await get_perm_group(cmd, message, mode_vars, node_name,
                                                                                   target_type)
                                if exc_tuple:
                                    bad_item = verify_targets(targets, exc_tuple, exc_group, node_name, target_type,
                                                              perms)
                                    if not bad_item:
                                        await cmd.db[cmd.db.db_nam].Permissions.update_one(
                                            {'server_id': message.guild.id}, {'$set': perms})
                                        await cmd.db.cache.del_cache(message.guild.id)
                                        if len(targets) > 1:
                                            title = f'✅ {len(targets)} {target_type} can no longer use `{node_name}`.'
                                        else:
                                            pnd = '#' if target_type == 'channels' else ''
                                            title = f'✅ {pnd}{targets[0].name} can no longer use `{node_name}`.'
                                        response = discord.Embed(color=0x77B255, title=title)
                                    else:
                                        pnd = '#' if target_type == 'channels' else ''
                                        title = f'⚠ {pnd}{bad_item.name} didn\'t have an override for `{node_name}`.'
                                        response = discord.Embed(color=0xFFCC4D, title=title)
                                else:
                                    perm_type = 'Command' if perm_mode == 'c' else 'Module'
                                    response = discord.Embed(color=0x696969, title=f'🔍 {perm_type} not found.')
                            else:
                                if targets:
                                    response = discord.Embed(color=0x696969, title=f'🔍 {targets} not found.')
                                else:
                                    ender = 'specified' if target_type == 'roles' else 'targeted'
                                    response = discord.Embed(color=0x696969, title=f'🔍 No {target_type} {ender}.')
                        else:
                            response = discord.Embed(color=0xBE1931,
                                                     title='❗ Unrecognized lookup mode, see usage example.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Invalid target type.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Separate permission type and name with a colon.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
