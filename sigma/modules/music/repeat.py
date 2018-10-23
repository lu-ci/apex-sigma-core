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


async def repeat(cmd: SigmaCommand, message: discord.Message, _args: list):
    if message.guild.voice_client:
        if message.author.voice:
            if message.guild.voice_client.channel.id == message.author.voice.channel.id:
                if message.guild.id in cmd.bot.music.repeaters:
                    cmd.bot.music.repeaters.remove(message.guild.id)
                    response = discord.Embed(color=0x3B88C3, title=f'➡ The queue will no longer repeat.')
                else:
                    cmd.bot.music.repeaters.append(message.guild.id)
                    response = discord.Embed(color=0x3B88C3, title=f'🔁 The queue will now repeat.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ You are not in my channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ I am not playing anything.')
    await message.channel.send(embed=response)
