"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import discord

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import error


async def customcommands(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    custom_commands = pld.settings.get('custom_commands')
    if custom_commands:
        custom_commands = sorted(list(custom_commands.keys()))
        cmd_count = len(custom_commands)
        page = pld.args[0] if pld.args else 1
        commands, page = PaginatorCore.paginate(custom_commands, page)
        start_range = (page - 1) * 10
        if commands:
            ender = 's' if cmd_count > 1 else ''
            summary = f'Showing **{len(commands)}** command{ender} from Page **#{page}**.'
            summary += f'\n{pld.msg.guild.name} has **{cmd_count}** custom command{ender}.'
            pfx = cmd.db.get_prefix(pld.settings)
            loop_index = start_range
            cmd_list_lines = []
            for key in commands:
                loop_index += 1
                list_line = f'**{loop_index}**: {pfx}{key}'
                cmd_list_lines.append(list_line)
            cmd_list = '\n'.join(cmd_list_lines)
            srv_color = await get_image_colors(pld.msg.guild.icon_url)
            response = discord.Embed(color=srv_color)
            response.set_author(name='Custom Commands', icon_url=pld.msg.guild.icon_url)
            response.add_field(name='Summary', value=summary, inline=False)
            response.add_field(name='Command List', value=cmd_list, inline=False)
        else:
            response = error('This page is empty.')
    else:
        response = error('This server has no custom commands.')
    await pld.msg.channel.send(embed=response)
