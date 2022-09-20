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

import hashlib
import json

import aiohttp
import discord
import ftfy
from lxml import html

from sigma.core.utilities.generic_responses import GenericResponse

osu_logo = 'https://i.imgur.com/hHAY7PM.png'
osu_modes = {'taiko': 1, 'catch': 2, 'mania': 3}


def make_url_hash(url):
    """
    Makes a quick md5 hash of the given URL.
    :type url: str
    :rtype: str
    """
    url_hash = hashlib.new('md5')
    url_hash.update(url.encode('utf-8'))
    return url_hash.hexdigest()


async def find_user_data(db, profile_url):
    """
    Scrapes the page to find the user's actual information.
    :type db: sigma.core.mechanics.database.Database
    :type profile_url: str
    :rtype: dict
    """
    cache_key = f'osu_profile_{make_url_hash(profile_url)}'
    data_cache = await db.cache.get_cache(cache_key)
    if not data_cache:
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as data:
                page = await data.text()
        osu_page_html = html.fromstring(page)
        osu_json_elem = osu_page_html.cssselect('.user_show div')
        user_data = {}
        if osu_json_elem:
            try:
                inner_data = osu_json_elem[0].attrib.get('data-initial-data')
                fixed_data = ftfy.fix_text(inner_data)
                user_data = json.loads(fixed_data)
            except (json.JSONDecodeError, IndexError, AttributeError, TypeError):
                pass
        await db.cache.set_cache(cache_key, user_data)
    else:
        user_data = data_cache
    return user_data


def get_name_and_mode(args):
    mode = 0
    if args[-1].startswith('--'):
        mode = osu_modes.get(args.pop()[2:].lower(), 0)
    name = '%20'.join(args)
    return name, mode


async def osu(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        osu_input, osu_mode = get_name_and_mode(pld.args)
        profile_url = f'https://osu.ppy.sh/users/{osu_input.lower()}'
        user_data = await find_user_data(cmd.db, profile_url)
        username = user_data.get('user').get('username')
        if username:
            user_color = str(pld.msg.author.color)[1:]
            sig_url = f'https://lemmmy.pw/osusig/sig.php?colour=hex{user_color}&uname={osu_input}&mode={osu_mode}'
            response = discord.Embed(color=pld.msg.author.color)
            response.set_image(url=sig_url)
            response.set_author(name=f'{username}\'s osu! Profile', url=profile_url, icon_url=osu_logo)
        else:
            response = GenericResponse('Profile not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
