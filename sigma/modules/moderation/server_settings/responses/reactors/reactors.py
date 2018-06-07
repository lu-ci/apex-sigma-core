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
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.paginate import paginate


async def reactors(cmd: SigmaCommand, message: discord.Message, args: list):
    reactor_files = await cmd.db.get_guild_settings(message.guild.id, 'ReactorTriggers')
    if reactor_files:
        reactor_list = sorted(list(reactor_files.keys()))
        reac_count = len(reactor_list)
        page = args[0] if args else 1
        triggers, page = paginate(reactor_list, page)
        start_range = (page - 1) * 10
        if triggers:
            ender = 's' if reac_count > 1 else ''
            summary = f'Showing **{len(triggers)}** trigger{ender} from Page **#{page}**.'
            summary += f'\n{message.guild.name} has **{reac_count}** reactor trigger{ender}.'
            loop_index = start_range
            trg_list_lines = []
            for key in triggers:
                loop_index += 1
                list_line = f'**{loop_index}**: {key}'
                trg_list_lines.append(list_line)
            trg_list = '\n'.join(trg_list_lines)
            srv_color = await get_image_colors(message.guild.icon_url)
            response = discord.Embed(color=srv_color)
            response.set_author(name='Automatic Reaction Triggers', icon_url=message.guild.icon_url)
            response.add_field(name='Summary', value=summary, inline=False)
            response.add_field(name='Trigger List', value=trg_list, inline=False)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ This page is empty.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ This server has no reaction triggers.')
    await message.channel.send(embed=response)
