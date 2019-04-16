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

import aiohttp
import discord
import hashlib

from sigma.core.utilities.generic_responses import error

osu_logo = 'http://w.ppy.sh/c/c9/Logo.png'


def make_url_hash(url):
    """
    Makes a quick md5 hash of the given URL.
    :param url: The URL to hash.
    :type url: str
    :return:
    :rtype: str
    """
    url_hash = hashlib.new('md5')
    url_hash.update(url.encode('utf-8'))
    return url_hash.hexdigest()


async def find_user_data(db, profile_url):
    """
    Scrapes the page to find the user's actual information.
    :param db: The main database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param profile_url: The user's profile URL.
    :type profile_url: str
    :return:
    :rtype: dict
    """
    cache_key = f'osu_profile_{make_url_hash(profile_url)}'
    data_cache = await db.cache.get_cache(cache_key)
    if not data_cache:
        async with aiohttp.ClientSession() as session:
            async with session.get(profile_url) as data:
                page = await data.text()
        lines = [x.strip() for x in page.split('\n')]
        lines.reverse()
        user_data = {}
        for line in lines:
            if line.startswith('{"id":'):
                try:
                    user_data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    pass
        await db.cache.set_cache(cache_key, user_data)
    else:
        user_data = data_cache
    return user_data


async def osu(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        osu_input = '%20'.join(pld.args)
        profile_url = f'https://osu.ppy.sh/users/{osu_input.lower()}'
        user_data = await find_user_data(cmd.db, profile_url)
        username = user_data.get('username')
        if username:
            user_color = str(pld.msg.author.color)[1:]
            sig_url = f'https://lemmmy.pw/osusig/sig.php?colour=hex{user_color}&uname={osu_input}'
            response = discord.Embed(color=pld.msg.author.color)
            response.set_image(url=sig_url)
            response.set_author(name=f'{username}\'s osu! Profile', url=profile_url, icon_url=osu_logo)
        else:
            response = error('Unable to retrieve profile.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
