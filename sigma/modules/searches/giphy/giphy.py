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


async def giphy(cmd: SigmaCommand, message: discord.Message, args: list):
    if 'api_key' and 'mashape_key' in cmd.cfg:
        api_key = cmd.cfg['api_key']
        mashape_key = cmd.cfg['mashape_key']
        if args:
            tag = '+'.join(args)
            url = f'https://giphy.p.mashape.com/v1/gifs/random?api_key={api_key}&tag={tag}'
            headers = {'X-Mashape-Key': mashape_key, 'Accept': 'application/json'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as data_response:
                    search_data = await data_response.read()
                    search_data = json.loads(search_data)
            data = search_data.get('data')
            if not data:
                response = discord.Embed(color=0x696969, title='🔍 No results')
            else:
                gif_id = data['id']
                gif_url = f'https://media.giphy.com/media/{gif_id}/giphy.gif'
                response = discord.Embed(color=0x00FF99).set_image(url=gif_url)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(None, embed=response)
    
