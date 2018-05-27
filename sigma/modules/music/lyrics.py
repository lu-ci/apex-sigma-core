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


import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


def parse_parts(lyr: str):
    pieces = []
    lines = lyr.split('\n\n')
    chunk = []
    for line in lines:
        if sum(len(c) for c in chunk) >= 1024:
            pieces.append("\n\n".join(chunk))
            chunk = []
        else:
            chunk.append(line)
    if chunk:
        pieces.append("\n\n".join(chunk))
    return pieces


async def lyrics(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        query = ' '.join(args)
    elif cmd.bot.music.currents.get(message.guild.id):
        query = cmd.bot.music.currents.get(message.guild.id).title
    else:
        query = None
    if query:
        qsplit = query.split('-')
        if len(qsplit) == 2:
            artist = qsplit[0].strip()
            song = qsplit[1].strip()
            api_url = f'https://lyric-api.herokuapp.com/api/find/{artist}/{song}'
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as data:
                    data = await data.read()
                    try:
                        data = json.loads(data).get('lyric')
                    except json.JSONDecodeError:
                        data = None
            if data:
                chunks = parse_parts(data)
                chunk_counter = 0
                for chunk in chunks:
                    chunk_counter += 1
                    chunk_title = f'🔖 Lyrics for {song} by {artist}'
                    if len(chunks) != 1:
                        chunk_title += f' Page {chunk_counter}/{len(chunks)}'
                    response = discord.Embed(color=0xf9f9f9, title=chunk_title)
                    response.description = chunk
                    await message.channel.send(embed=response)
                return
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Nothing found for {song} by {artist}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Make sure to separate the artist and song with a dash.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No song information given, and nothing currently playing.')
    await message.channel.send(embed=response)
