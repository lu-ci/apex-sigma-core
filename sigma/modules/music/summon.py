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

from concurrent.futures import TimeoutError

import discord

from sigma.core.utilities.generic_responses import error


async def summon(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.voice:
        me = pld.msg.guild.me
        vc = pld.msg.author.voice.channel
        if me.permissions_in(vc).connect:
            if me.permissions_in(vc).speak:
                if pld.msg.guild.voice_client:
                    if pld.msg.author.voice.channel.id != pld.msg.guild.voice_client.channel.id:
                        await pld.msg.guild.voice_client.move_to(pld.msg.author.voice.channel)
                        title = f'🚩 Moved to {pld.msg.author.voice.channel.name}.'
                        response = discord.Embed(color=0xdd2e44, title=title)
                    else:
                        response = error('We are in the same channel.')
                else:
                    try:
                        await pld.msg.author.voice.channel.connect(reconnect=False)
                        title = f'🚩 Connected to {pld.msg.author.voice.channel.name}.'
                        response = discord.Embed(color=0xdd2e44, title=title)
                    except TimeoutError:
                        if pld.msg.guild.voice_client:
                            await pld.msg.guild.voice_client.disconnect()
                        response = error('I timed out while trying to connect.')
            else:
                response = error(f'I am not allowed to speak in {vc.name}.')
        else:
            response = error(f'I am not allowed to connect to {vc.name}.')
    else:
        response = error('You are not in a voice channel.')
    await pld.msg.channel.send(embed=response)
