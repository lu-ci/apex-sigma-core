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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def repeat(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.guild.voice_client:
        if pld.msg.author.voice:
            if pld.msg.guild.voice_client.channel.id == pld.msg.author.voice.channel.id:
                if pld.msg.guild.id in cmd.bot.music.repeaters:
                    cmd.bot.music.repeaters.remove(pld.msg.guild.id)
                    response = discord.Embed(color=0x3B88C3, title='➡ The queue will no longer repeat.')
                else:
                    cmd.bot.music.repeaters.append(pld.msg.guild.id)
                    response = discord.Embed(color=0x3B88C3, title='🔁 The queue will now repeat.')
            else:
                response = error('You are not in my channel.')
        else:
            response = error('You are not in a voice channel.')
    else:
        response = error('I am not playing anything.')
    await pld.msg.channel.send(embed=response)
