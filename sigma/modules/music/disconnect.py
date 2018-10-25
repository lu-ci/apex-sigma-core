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
from sigma.core.utilities.data_processing import user_avatar


async def disconnect(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                if message.guild.id in cmd.bot.music.queues:
                    del cmd.bot.music.queues[message.guild.id]
                response = discord.Embed(color=0x66CC66, title='✅ Disconnected and purged.')
                requester = f'{message.author.name}#{message.author.discriminator}'
                response.set_author(name=requester, icon_url=user_avatar(message.author))
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)
