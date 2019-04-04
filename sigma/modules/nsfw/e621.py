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

import json
import secrets

import aiohttp
import discord

from sigma.core.utilities.generic_responses import not_found


async def e621(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    url = 'https://e621.net/post/index.json?tags='
    url += '+'.join(pld.args) if pld.args else 'nude'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as data:
            data = await data.read()
            data = json.loads(data)
    if data:
        post = secrets.choice(data)
        image_url = post['file_url']
        icon_url = 'https://e621.net/favicon.ico'
        post_url = f'https://e621.net/post/show/{post["id"]}'
        response = discord.Embed(color=0x152F56)
        response.set_author(name='e621', url=post_url, icon_url=icon_url)
        response.set_image(url=image_url)
        response.set_footer(text=f'Score: {post["score"]} | Size: {post["width"]}x{post["height"]}')
    else:
        response = not_found('No results.')
    await pld.msg.channel.send(embed=response)
