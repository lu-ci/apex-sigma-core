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

import secrets

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def cat(cmd: SigmaCommand, message: discord.Message, args: list):
    if 'api_key' in cmd.cfg:
        cat_api_key = cmd.cfg['api_key']
        api_url = f'http://thecatapi.com/api/images/get?format=xml&results_per_page=100&api_key={cat_api_key}'
    else:
        api_url = f'http://thecatapi.com/api/images/get?format=xml&results_per_page=100'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as raw_page:
            results = html.fromstring(await raw_page.text())[0][0]
    choice = secrets.choice(results)
    image_url = str(choice[0].text)
    embed = discord.Embed(color=0xFFDC5D, title='🐱 Meow~')
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
