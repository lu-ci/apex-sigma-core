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
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.data_processing import get_image_colors


async def customcommands(cmd: SigmaCommand, pld: CommandPayload):
    custom_commands = await cmd.db.get_guild_settings(message.guild.id, 'custom_commands')
    if custom_commands:
        custom_commands = sorted(list(custom_commands.keys()))
        cmd_count = len(custom_commands)
        page = args[0] if args else 1
        commands, page = PaginatorCore.paginate(custom_commands, page)
        start_range = (page - 1) * 10
        if commands:
            ender = 's' if cmd_count > 1 else ''
            summary = f'Showing **{len(commands)}** command{ender} from Page **#{page}**.'
            summary += f'\n{message.guild.name} has **{cmd_count}** custom command{ender}.'
            pfx = await cmd.db.get_prefix(message)
            loop_index = start_range
            cmd_list_lines = []
            for key in commands:
                loop_index += 1
                list_line = f'**{loop_index}**: {pfx}{key}'
                cmd_list_lines.append(list_line)
            cmd_list = '\n'.join(cmd_list_lines)
            srv_color = await get_image_colors(message.guild.icon_url)
            response = discord.Embed(color=srv_color)
            response.set_author(name='Custom Commands', icon_url=message.guild.icon_url)
            response.add_field(name='Summary', value=summary, inline=False)
            response.add_field(name='Command List', value=cmd_list, inline=False)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ This page is empty.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ This server has no custom commands.')
    await message.channel.send(embed=response)
