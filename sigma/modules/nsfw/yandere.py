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
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def yandere(cmd: SigmaCommand, message: discord.Message, args: list):
    url_base = 'https://yande.re/post.json?limit=100&tags='
    if not args:
        tags = 'nude'
    else:
        tags = '+'.join(args)
    url = url_base + tags
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
            data = json.loads(data)
    if len(data) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        post = secrets.choice(data)
        image_url = post['file_url']
        icon_url = 'https://i.imgur.com/vgJwau2.png'
        post_url = f'https://yande.re/post/show/{post["id"]}'
        embed = discord.Embed(color=0xad3d3d)
        embed.set_author(name='Yande.re', url=post_url, icon_url=icon_url)
        embed.set_image(url=image_url)
        embed.set_footer(
            text=f'Score: {post["score"]} | Size: {post["width"]}x{post["height"]} | Uploaded By: {post["author"]}')
    await message.channel.send(None, embed=embed)
