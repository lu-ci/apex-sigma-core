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

from sigma.core.utilities.generic_responses import error, not_found

tdoll_data = []
tdoll_root = None
gf_icon = 'https://en.gfwiki.com/images/c/c9/Logo.png'
gf_color = 0xffcc4d


def get_rarity(elem):
    """

    :param elem:
    :type elem:
    :return:
    :rtype:
    """
    rarities = {
        5: 'ffcd4a',
        4: 'd6e35a',
        3: '6bdfce'
    }
    out_val = 2
    for rarity_val in rarities.keys():
        rarity_color = rarities.get(rarity_val)
        if elem.attrib.get('style', '').lower().startswith(f'color: #{rarity_color}'):
            out_val = rarity_val
            break
    return out_val


def make_doll_data(row):
    """

    :param row:
    :type row:
    """
    prod_time = ':'.join(row[0].text.split(':')[:-1]).strip()
    dolls = row[1]
    for doll in dolls:
        name_split = doll[0].text_content().split()
        doll_type = name_split[0].lower()
        doll_name = ' '.join(name_split[1:])
        doll_url = f"https://en.gfwiki.com{doll.attrib.get('href')}"
        doll_rarity = get_rarity(doll[0])
        ddata = {'name': doll_name, 'time': prod_time, 'url': doll_url, 'rarity': doll_rarity, 'type': doll_type}
        tdoll_data.append(ddata)


async def fill_tdoll_data():
    global tdoll_root
    async with aiohttp.ClientSession() as session:
        async with session.get('https://en.gfwiki.com/wiki/T-Doll_Production') as data:
            page = await data.text()
    tdoll_root = lx.fromstring(page)
    mct = tdoll_root.cssselect('.multi-column-table')
    rows = mct[0][0]
    for row in rows:
        make_doll_data(row)
    tdoll_data.sort(key=lambda tdd: tdd.get('name'), reverse=True)
    tdoll_data.sort(key=lambda tdd: tdd.get('rarity'), reverse=True)


async def gftdollproduction(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not tdoll_data:
        await fill_tdoll_data()
    if pld.args:
        time_q = pld.args[0].lower()
        dolls = [di for di in tdoll_data if di.get('time') == time_q]
        if dolls:
            lines = [rf'{d.get("rarity")}\* {d.get("type").upper()} - **{d.get("name")}**' for d in dolls]
            response = discord.Embed(color=gf_color)
            response.set_author(name='Girls Frontline: T-Doll Production', icon_url=gf_icon)
            response.description = '\n'.join(lines)
        else:
            response = not_found('Nothing found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
