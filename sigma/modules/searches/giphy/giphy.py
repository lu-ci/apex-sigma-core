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
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand

giphy_icon = 'https://i.imgur.com/tmDySRu.gif'


async def giphy(cmd: SigmaCommand, pld: CommandPayload):
    api_key = cmd.cfg.get('api_key')
    if api_key:
        if args:
            qry = ' '.join(args)
            url = f'https://api.giphy.com/v1/gifs/search?q={qry}&api_key={api_key}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data_response:
                    search_data = await data_response.read()
                    search_data = json.loads(search_data)
            data = search_data.get('data')
            if data:
                data = secrets.choice(data)
                gif_id = data.get('id')
                gif_url = f'https://media.giphy.com/media/{gif_id}/giphy.gif'
                response = discord.Embed(color=0x262626)
                response.set_image(url=gif_url)
                response.set_footer(icon_url=giphy_icon, text='Powered By GIPHY.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No results')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
