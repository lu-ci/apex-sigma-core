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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, ok


async def disconnect(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.voice:
        same_bound = True
        if pld.msg.guild.voice_client:
            if pld.msg.guild.voice_client.channel.id != pld.msg.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if pld.msg.guild.voice_client:
                await pld.msg.guild.voice_client.disconnect()
                if pld.msg.guild.id in cmd.bot.music.queues:
                    del cmd.bot.music.queues[pld.msg.guild.id]
                response = ok('Disconnected and purged.')
                requester = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                response.set_author(name=requester, icon_url=user_avatar(pld.msg.author))
            else:
                response = error('I am not connected to any channel.')
        else:
            response = error('You are not in my voice channel.')
    else:
        response = error('You are not in a voice channel.')
    await pld.msg.channel.send(embed=response)
