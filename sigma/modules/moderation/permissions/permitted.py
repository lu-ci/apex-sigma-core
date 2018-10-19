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
from sigma.modules.moderation.permissions.permit import get_target_type


def get_exceptions(message: discord.Message, exceptions: list, target_type: str):
    overridden_items = []
    guild_dict = {'channels': message.guild.channels, 'users': message.guild.members, 'roles': message.guild.roles}
    guild_items = guild_dict.get(target_type)
    for exc_chn_id in exceptions:
        pnd = '#' if target_type == 'channels' else ''
        exc_item = discord.utils.find(lambda c: c.id == exc_chn_id, guild_items)
        exc_item_name = f'{pnd}{exc_item.name}' if exc_item else str(exc_chn_id)
        overridden_items.append(exc_item_name)
    return overridden_items


async def permitted(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            if ':' in args[1]:
                target_type = get_target_type(args[0].lower())
                if target_type:
                    perm_mode = args[1].split(':')[0]
                    node_name = args[1].split(':')[1]
                    modes = {
                        'c': ('Command', 'command_exceptions', cmd.bot.modules.commands, True),
                        'm': ('Module', 'module_exceptions', cmd.bot.modules.categories, False)
                    }
                    perms = await get_all_perms(cmd.db, message)
                    mode_vars = modes.get(perm_mode)
                    if mode_vars:
                        mode_name, exception_group, check_group, check_alts = mode_vars
                        if check_alts:
                            if node_name in cmd.bot.modules.alts:
                                node_name = cmd.bot.modules.alts[node_name]
                        if node_name in check_group:
                            exceptions = perms.get(exception_group, {}).get(node_name, {}).get(target_type, [])
                            overridden_items = get_exceptions(message, exceptions, target_type)
                            if overridden_items:
                                total_overrides = len(overridden_items)
                                page = args[2] if len(args) > 2 else 1
                                overrides, page = paginate(overridden_items, page, 50)
                                title = f'{message.guild.name} {node_name.upper()} {target_type[:-1].title()} Overrides'
                                info = f'[Page {page}] Showing {len(overrides)} out of {total_overrides} channel overrides.'
                                response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
                                response.set_author(name=title, icon_url=message.guild.icon_url)
                                response.description = ', '.join(overrides)
                                response.set_footer(text=info)
                            else:
                                title = f'🔍 No {target_type[:-1]} overrides found for {node_name}.'
                                response = discord.Embed(color=0x696969, title=title)
                        else:
                            response = discord.Embed(color=0x696969, title=f'🔍 No {node_name} {mode_name.lower()} found.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Unrecognized lookup mode, see usage example.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid target type.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Separate permission type and name with a colon.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
