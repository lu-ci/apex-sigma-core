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


async def konachan(cmd, message, args):
    url_base = 'https://konachan.com/post.json?limit=100&tags='
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
        post_url = f'http://konachan.com/post/show/{post["id"]}'
        icon_url = 'https://i.imgur.com/qc4awFL.png'
        embed = discord.Embed(color=0x473a47)
        embed.set_author(name='Konachan', url=post_url, icon_url=icon_url)
        embed.set_image(url=post["file_url"])
        embed.set_footer(
            text=f'Score: {post["score"]} | Size: {post["width"]}x{post["height"]} | Uploaded By: {post["author"]}')
    await message.channel.send(None, embed=embed)
