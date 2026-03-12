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

import aiohttp
import discord
from lxml import html as lx

from sigma.core.utilities.generic_responses import GenericResponse

tdoll_page_index = {}
tdoll_pages = {}
tdoll_colors = {
    '2': 0xffffff,
    '3': 0x68dec9,
    '4': 0xd2de61,
    '5': 0xfda82e,
    'EXTRA': 0xdfb6ff
}
gf_icon = 'https://en.gfwiki.com/images/c/c9/Logo.png'
stat_coords = {
    'health': [0, 0, 1, 0],
    'ammo': [0, 0, 1, 1],
    'rations': [0, 0, 1, 2],
    'damage': [1, 0, 0, 1],
    'evasion': [1, 0, 0, 3],
    'accuracy': [1, 0, 1, 1],
    'rate of fire': [1, 0, 1, 3],
    'move speed': [1, 0, 2, 1],
    'armor': [1, 0, 2, 3],
    'crit. rate': [1, 0, 3, 1],
    'crit. damage': [1, 0, 3, 3],
    'amor pen.': [1, 0, 4, 1]
}


async def fill_tdoll_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://en.gfwiki.com/wiki/T-Doll_Index') as data:
            page = await data.text()
    root = lx.fromstring(page)
    cards = root.cssselect('.card-bg-small')
    for card in cards:
        name = card[0][0].attrib.get('title').strip().lower()
        page = f"https://en.gfwiki.com{card[0][0].attrib.get('href')}"
        index = card[2].text.strip()
        tdoll_page_index.update({name: page, index: page})


def get_profile_info(root):
    """
    :type root:
    :rtype: dict
    """
    data = {}
    pbox = root.cssselect('.profiletable')[0]
    for row in pbox:
        if len(row) == 2:
            key = row[0].text.strip().lower().replace(' ', '_')
            val = row[1].text.strip()
            if key and val:
                data.update({key: val})
    return data


async def get_tdoll_data(url):
    """
    :type url: str
    :rtype: dict
    """
    tdoll_data = tdoll_pages.get(url)
    if not tdoll_data:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                page = await data.text()
        root = lx.fromstring(page)
        tdoll_name = root.cssselect('.dollname')[0].text.strip()
        tdoll_image = root.cssselect('.dollprofileimage')[0].attrib.get('src')
        tdoll_rarity = root.cssselect('.raritystars')[0].attrib.get('class').split('rarity')[-1]
        tdoll_data = {
            'name': tdoll_name,
            'image': tdoll_image,
            'rarity': tdoll_rarity,
        }
        tdoll_data.update(get_profile_info(root))
        tdoll_data.update({'stats': get_tdoll_stats(root)})
        tdoll_pages.update({url: tdoll_data})
    return tdoll_data


def get_weapon_info_block(data):
    """
    :type data: dict
    :rtype: str
    """
    out = f'**Full Name**: {data.get("full_name", "Unknown")}'
    out += f'\n**Manufacturer**: {data.get("manufacturer", "Unknown")}'
    out += f'\n**Country of Origin**: {data.get("country_of_origin", "Unknown")}'
    return out


def get_tdoll_stats(root):
    """
    :type root:
    :rtype: dict
    """
    sr = root.cssselect('.stattabcontainer')[0][0][0]
    data = {}
    for key in stat_coords:
        coords = stat_coords.get(key)
        curr_elem = sr
        for coor in coords:
            curr_elem = curr_elem[coor]
        data.update({key: curr_elem.text_content().strip().replace('\n', ' ')})
    return data


def get_weapon_satats_block(data):
    """
    :type data: dict
    :rtype: str
    """
    stats = data.get('stats')
    lines = []
    for key in stats.keys():
        kn = key.title()
        lines.append(f'**{kn}**: {stats.get(key)}')
    return '\n'.join(lines)


async def gftacticaldoll(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not tdoll_page_index:
        await fill_tdoll_data()
    if pld.args:
        tdoll_search = ' '.join(pld.args)
        tdoll_url = tdoll_page_index.get(tdoll_search.lower())
        if tdoll_url:
            tdoll_data = await get_tdoll_data(tdoll_url)
            response = discord.Embed(color=tdoll_colors.get(tdoll_data.get('rarity')))
            response.set_image(url=tdoll_data.get('image'))
            response.set_author(name=f'Girls Frontline: {tdoll_data.get("name")}', icon_url=gf_icon, url=tdoll_url)
            response.add_field(name='Weapon Information', value=get_weapon_info_block(tdoll_data), inline=False)
            response.add_field(name='Weapon Statistics', value=get_weapon_satats_block(tdoll_data), inline=False)
        else:
            response = GenericResponse('Nothing found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
