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

from concurrent.futures import TimeoutError

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def summon(_cmd: SigmaCommand, pld: CommandPayload):
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
                        response = discord.Embed(color=0xBE1931, title='❗ We are in the same channel.')
                else:
                    try:
                        await pld.msg.author.voice.channel.connect(reconnect=False)
                        title = f'🚩 Connected to {pld.msg.author.voice.channel.name}.'
                        response = discord.Embed(color=0xdd2e44, title=title)
                    except TimeoutError:
                        if pld.msg.guild.voice_client:
                            await pld.msg.guild.voice_client.disconnect()
                        response = discord.Embed(color=0xBE1931, title='❗ I timed out while trying to connect.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to speak in {vc.name}.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to connect to {vc.name}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await pld.msg.channel.send(embed=response)
