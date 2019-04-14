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

from sigma.core.utilities.generic_responses import not_found


async def fill_r34_cache(db, tags):
    """
    Fills the rule34 cache with images from the given search criteria.
    :param db: The main database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param tags: The tags to fill the cache for.
    :type tags: str
    """
    cache_key = f'rule34_{tags}'
    r34_url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags
    async with aiohttp.ClientSession() as session:
        async with session.get(r34_url) as data:
            data = await data.read()
            posts = html.fromstring(data)
            posts = [dict(ps.attrib) for ps in posts if ps.attrib.get('file_url')]
            await db.cache.set_cache(cache_key, posts)


async def rule34(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    tags = '+'.join(pld.args) if pld.args else 'nude'
    cache_key = f'rule34_{tags}'
    collect_needed = False if await cmd.db.cache.get_cache(cache_key) else True
    if collect_needed:
        await fill_r34_cache(cmd.db, tags)
    collection = await cmd.db.cache.get_cache(cache_key)
    if collection:
        choice = secrets.choice(collection)
        img_url = choice.get('file_url')
        if not img_url.startswith('http'):
            img_url = f"https:{choice.get('file_url')}"
        icon_url = 'https://i.imgur.com/63GGrmG.png'
        post_url = f'https://rule34.xxx/index.php?page=post&s=view&id={choice.get("id")}'
        footer_text = f'Score: {choice.get("score")} | Size: {choice.get("width")}x{choice.get("height")}'
        response = discord.Embed(color=0xaae5a3)
        response.set_author(name='Rule 34', url=post_url, icon_url=icon_url)
        response.set_image(url=img_url)
        response.set_footer(text=footer_text)
    else:
        response = not_found('No results.')
    await pld.msg.channel.send(embed=response)
