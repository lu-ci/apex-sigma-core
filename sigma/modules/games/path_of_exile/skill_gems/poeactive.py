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

import aiohttp
import discord
import lxml.html as lx

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import get_image_colors

gem_list_cache = {}
gem_data_cache = {}


async def fill_gem_cache():
    if not gem_list_cache:
        active_sg_url = 'https://pathofexile.gamepedia.com/List_of_active_skill_gems'
        async with aiohttp.ClientSession() as session:
            async with session.get(active_sg_url) as data:
                page_html_raw = await data.text()
        page_html = lx.fromstring(page_html_raw)
        gem_items = page_html.cssselect('.c-item-hoverbox')
        for gem_item in gem_items:
            gem_name = gem_item[0][1].text
            gem_dkey = gem_name.replace(' ', '_').lower()
            url_pointer = gem_item[0][1].attrib.get("href")
            gem_link = f'https://pathofexile.gamepedia.com/{url_pointer}'
            gem_list_cache.update({gem_dkey: {'name': gem_name, 'url': gem_link}})


async def get_gem_data(gem_name: str, gem_url: str):
    gem_key = gem_name.replace(' ', '_').lower()
    gem_data = gem_data_cache.get(gem_key)
    if not gem_data:
        async with aiohttp.ClientSession() as session:
            async with session.get(gem_url) as data:
                page_html_raw = await data.text()
        page_html = lx.fromstring(page_html_raw)
        isb = page_html.cssselect('.item-stats')[0]
        gem_info = "\n".join([row.text_content().strip() for row in isb[0]])
        try:
            gem_level = int(isb[1][0][0][0].text or 0)
        except IndexError:
            gem_level = 0
        gem_desc = isb[2].text
        gem_image = page_html.cssselect(".image")[1][0].attrib.get("src")
        spell_image = page_html.cssselect(".image")[0][0].attrib.get("src")
        gem_data = {
            'name': gem_name,
            'url': gem_url,
            'info': parse_gem_info(gem_info),
            'level': gem_level,
            'desc': gem_desc,
            'image': {
                'gem': gem_image,
                'spell': spell_image
            }
        }
        gem_data_cache.update({gem_key: gem_data})
    return gem_data


def find_broad(lookup: str):
    out = None
    for key in gem_list_cache:
        if lookup in key:
            out = gem_list_cache.get(key)
            break
    return out


def parse_gem_info(gem_info: str):
    sects = gem_info.split('\n\n')
    types = sects[0].split('\n')
    det_sects = sects[1:]
    info_lines = []
    for det_sect in det_sects:
        if ': ' in det_sect:
            info_name = det_sect.split(': ')[0].strip()
            info_value = det_sect.split(': ')[1].strip()
            info_lines.append([info_name, info_value])
    return {'types': types, 'details': info_lines}


async def poeactive(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup_key = '_'.join(args).lower()
        await fill_gem_cache()
        gem_entry = gem_list_cache.get(lookup_key) or find_broad(lookup_key)
        if gem_entry:
            gem_data = await get_gem_data(gem_entry.get('name'), gem_entry.get('url'))
            if gem_data:
                if gem_data.get('level'):
                    gem_info_block = f'**Level**: {gem_data.get("level")}'
                else:
                    gem_info_block = ''
                for detail in gem_data.get('info').get('details'):
                    gem_info_block += f'\n**{detail[0]}**: {detail[1]}'
                img_data = gem_data.get('image')
                gem_img: str = img_data.get('gem')
                spell_img: str = img_data.get('spell')
                title = f'Active Skill Gem: {gem_data.get("name")}'
                response = discord.Embed(color=await get_image_colors(spell_img))
                response.description = gem_data.get('desc')
                response.set_thumbnail(url=spell_img)
                response.set_author(name=title, icon_url=gem_img, url=gem_data.get('url'))
                response.add_field(name='Information', value=gem_info_block, inline=False)
                response.set_footer(text=f'Types: {" | ".join(gem_data.get("info").get("types"))}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid gem data received.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Gem not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
