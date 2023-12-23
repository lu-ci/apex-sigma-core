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
from sigma.core.utilities.generic_responses import GenericResponse


async def reactors(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    reactor_files = pld.settings.get('reactor_triggers')
    if reactor_files:
        reactor_list = sorted(list(reactor_files.keys()))
        react_count = len(reactor_list)
        page = pld.args[0] if pld.args else 1
        triggers, page = PaginatorCore.paginate(reactor_list, page)
        start_range = (page - 1) * 10
        if triggers:
            ender = 's' if react_count > 1 else ''
            summary = f'Showing **{len(triggers)}** trigger{ender} from Page **#{page}**.'
            summary += f'\n{pld.msg.guild.name} has **{react_count}** reactor trigger{ender}.'
            loop_index = start_range
            trg_list_lines = []
            for key in triggers:
                loop_index += 1
                list_line = f'**{loop_index}**: {key.lower()}'
                trg_list_lines.append(list_line)
            trg_list = '\n'.join(trg_list_lines)
            guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon else None
            srv_color = await get_image_colors(guild_icon)
            response = discord.Embed(color=srv_color)
            response.set_author(name='Automatic Reaction Triggers', icon_url=guild_icon)
            response.add_field(name='Summary', value=summary, inline=False)
            response.add_field(name='Trigger List', value=trg_list, inline=False)
        else:
            response = GenericResponse('This page is empty.').error()
    else:
        response = GenericResponse('This server has no reaction triggers.').error()
    await pld.msg.channel.send(embed=response)
