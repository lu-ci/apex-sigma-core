# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


async def spelledlike(cmd, message, args):
    # strip spaces from args
    print(args)
    args = list(filter(lambda a: a != '', args))
    print(args)
    response = discord.Embed()
    if args:
        query = ' '.join(args)
        print(query)
        site_url = f'http://www.rhymezone.com/r/rhyme.cgi?Word={query}&typeofrhyme=spell'
        api_url = f'https://api.datamuse.com/words?sp={query}&max=11'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data_response:
                data = await data_response.read()
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    data = []

        data = list(filter(lambda r: 'score' in r, data))
        if data:
            data = list(map(lambda r: '- ' + r['word'], data))
            response.set_author(name=f'Words that spelled like {query}', url=site_url,
                                icon_url='https://i.imgur.com/GKM6AMT.png')
            response.colour = 0xFBB429
            response.description = '\n'.join(data[:10])
            if len(data) > 10:
                response.set_footer(text='Follow the link in the title to see more')
        else:
            response.title = '🔍 No results.'
            response.colour = 0x696969
    else:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931

    await message.channel.send(embed=response)
