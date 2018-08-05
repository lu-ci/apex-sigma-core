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
from sigma.core.utilities.data_processing import paginate, get_image_colors
from sigma.modules.moderation.permissions.nodes.permission_data import get_all_perms


async def permittedroles(cmd: SigmaCommand, message: discord.Message, args: list):
    has_args = False if not args else False if ':' not in args[-1] else True
    page_num = args[0] if args else 1
    if has_args:
        modes = {
            'c': ('Command', 'command_exceptions', cmd.bot.modules.commands, True),
            'm': ('Module', 'module_exceptions', cmd.bot.modules.categories, False)
        }
        perms = await get_all_perms(cmd.db, message)
        perm_mode, node_name = [piece.lower() for piece in args[-1].split(':')]
        mode_vars = modes.get(perm_mode)
        if mode_vars:
            overridden_roles = []
            mode_name, exception_group, check_group, check_alts = mode_vars
            if check_alts:
                if node_name in cmd.bot.modules.alts:
                    node_name = cmd.bot.modules.alts[node_name]
            if node_name in check_group:
                exceptions = perms.get(exception_group, {}).get(node_name, {}).get('roles', [])
                for exc_rl_id in exceptions:
                    exc_rl = discord.utils.find(lambda r: r.id == exc_rl_id, message.guild.roles)
                    exc_rl_name = f'{exc_rl.name}' if exc_rl else str(exc_rl_id)
                    overridden_roles.append(exc_rl_name)
                if overridden_roles:
                    total_overrides = len(overridden_roles)
                    overrides, page = paginate(overridden_roles, page_num, 50)
                    title = f'{message.guild.name} {node_name.upper()} Role Overrides'
                    info_text = f'[Page {page}] Showing {len(overrides)} out of {total_overrides} disabled modules.'
                    response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
                    response.set_author(name=title, icon_url=message.guild.icon_url)
                    response.description = ', '.join(overrides)
                    response.set_footer(text=info_text)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 No overridden roles found for {node_name}.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 No {node_name} {mode_name.lower()} found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Unrecognized lookup mode, see usage example.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
