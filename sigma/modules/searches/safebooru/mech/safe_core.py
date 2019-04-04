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

import secrets

import aiohttp
import discord
from lxml import html


async def grab_post_list(tags):
    links = []
    for x in range(0, 20):
        resource = f'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=rating:safe+{tags}&pid={x}'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            if 'file_url' in post.attrib:
                file_url = post.attrib['file_url']
                extension = file_url.split('.')[-1]
                if extension in ['png', 'jpg', 'jpeg', 'gif']:
                    height = int(post.attrib['height'])
                    width = int(post.attrib['width'])
                    if width < 2000 and height < 2000:
                        links.append(post)
    return links


def generate_embed(post, titles, color=0xff6699, icon='https://i.imgur.com/WQbzk9y.png'):
    image_url = post.attrib['file_url']
    image_source = f'http://safebooru.org/index.php?page=post&s=view&id={post.attrib["id"]}'
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    response = discord.Embed(color=color)
    response.set_author(name=secrets.choice(titles), icon_url=icon, url=image_source)
    response.set_image(url=image_url)
    response.set_footer(
        text=f'Score: {post.attrib["score"]} | Size: {post.attrib["width"]}x{post.attrib["height"]}')
    return response
