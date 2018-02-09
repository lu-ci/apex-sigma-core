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

import secrets

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def safebooru(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        tag = 'cute'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    resource = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=' + tag
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
    posts = html.fromstring(data)
    if len(posts) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 Nothing found.')
    else:
        choice = secrets.choice(posts)
        image_url = choice.attrib['file_url']
        icon_url = 'https://i.imgur.com/3Vb6LdJ.png'
        post_url = f'http://safebooru.org/index.php?page=post&s=view&id={choice.attrib["id"]}'
        if image_url.startswith('//'):
            image_url = 'http:' + image_url
        embed = discord.Embed(color=0x8bb2a7)
        embed.set_author(name='Safebooru', icon_url=icon_url, url=post_url)
        embed.set_image(url=image_url)
        embed.set_footer(
            text=f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}')
    await message.channel.send(None, embed=embed)
