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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import get_image_colors
from sigma.modules.utilities.information import guild_watcher


async def serverstatistics(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    gld_stats = guild_watcher.stats.get(pld.msg.guild.id, {})
    start_time = arrow.get(guild_watcher.start_stamp)
    time_dif = arrow.utcnow().timestamp - start_time.timestamp
    command_rate = str(gld_stats.get("commands", 0) / time_dif)[:5]
    message_rate = str(gld_stats.get("messages", 0) / time_dif)[:5]
    pop_text = f'Channels: **{len(pld.msg.guild.channels)}**'
    pop_text += f'\nRoles: **{len(pld.msg.guild.roles)}**'
    pop_text += f'\nMembers: **{pld.msg.guild.member_count}**'
    pop_text += f'\nBots: **{len([u for u in pld.msg.guild.members if u.bot])}**'
    exec_text = f'Commands: **{gld_stats.get("commands", 0)}**'
    exec_text += f'\nCommand Rate: **{command_rate}/s**'
    exec_text += f'\nMessages: **{gld_stats.get("messages", 0)}**'
    exec_text += f'\nMessage Rate: **{message_rate}/s**'
    color = await get_image_colors(pld.msg.guild.icon_url)
    response = discord.Embed(color=color, timestamp=arrow.get(start_time).datetime)
    response.set_author(name=f'{pld.msg.guild.name} Statistics', icon_url=pld.msg.guild.icon_url)
    response.add_field(name='Population', value=pop_text)
    response.add_field(name='Usage', value=exec_text)
    response.set_footer(text=f'Tracking since {start_time.humanize()}')
    await pld.msg.channel.send(embed=response)
