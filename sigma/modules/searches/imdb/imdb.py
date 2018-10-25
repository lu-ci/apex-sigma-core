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


async def imdb(_cmd: SigmaCommand, pld: CommandPayload):
    if args:
        search = '%20'.join(args)
        api_url = f'http://sg.media-imdb.com/suggests/{search[0].lower()}/{search}.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data:
                search_data = await data.text()
                search_data = '('.join(search_data.split("(")[1:])[:-1]
                data = json.loads(search_data, encoding='utf-8')
                data = data.get('d', [None])[0]
        if data:
            imdb_icon = 'https://ia.media-imdb.com/images/G/01/imdb/images/mobile/'
            imdb_icon += 'apple-touch-icon-web-152x152-1475823641._CB522736557_.png'
            title = data.get('l', 'Unknown')
            staring = data.get('s', 'Unknown')
            movie_id = data.get('id')
            year = data.get('y', 'Unknown')
            image = data.get('i', [None])[0]
            imdb_movie_url = f'http://www.imdb.com/title/{movie_id}/'
            movie_desc = f'IMDB Page: [Here]({imdb_movie_url})'
            movie_desc += f'\nRelease Year: {year}'
            movie_desc += f'\nStaring: {staring}'
            response = discord.Embed(color=0xebc12d)
            response.add_field(name=title, value=movie_desc)
            response.set_footer(text='From the Internet Movie DataBase.', icon_url=imdb_icon)
            if image:
                response.set_thumbnail(url=image)
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
