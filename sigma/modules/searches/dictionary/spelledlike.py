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

icon = 'https://i.imgur.com/GKM6AMT.png'


async def spelledlike(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        query = '+'.join(args).lower()
        site_url = f'http://www.rhymezone.com/r/rhyme.cgi?Word={query}&typeofrhyme=spell'
        api_url = f'https://api.datamuse.com/words?sp={query}&max=11'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data_response:
                data = await data_response.read()
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    data = {}
        data = [r for r in data if 'score' in r]
        if data:
            data = [f'- {item.get("word")}' for item in data]
            response = discord.Embed(color=0xFBB429, title='\n'.join(data[:10]))
            response.set_author(name=f'Words that spelled like {query.replace("+", " ")}', url=site_url, icon_url=icon)
            if len(data) > 10:
                response.set_footer(text='Follow the link in the title to see more.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
