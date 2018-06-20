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
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def kanji(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        query = args[0][0]
        async with aiohttp.ClientSession() as session:
            async with session.get('http://classic.jisho.org/kanji/details/' + query) as data:
                rq_text = await data.text()
        if not rq_text.find('503 Service Unavailable') != -1:
            kanji_data = html.fromstring(rq_text).cssselect('.kanji_result')
            if kanji_data:
                search_url = f'http://jisho.org/search/{query}%20%23kanji'
                jisho_icon = 'https://i.imgur.com/X1fCJLV.png'
                kanji_page = kanji_data[0]
                stroke_source = kanji_page.cssselect('.stroke_diagram img')[0].attrib.get('src')
                kanji_data = {
                    'kanji': kanji_page.cssselect('.literal.japanese')[0].text.strip(),
                    'strokes': kanji_page.cssselect('.specs strong')[0].text,
                    'stroke order': f'http://classic.jisho.org{stroke_source}',
                    'meta': {'radical': None, 'parts': [], 'variants': []},
                    'readings': {'kun': [], 'on': [], 'names': []},
                    'meanings': []
                }
                # Parse radical and parts data
                for element in kanji_page.cssselect('.connections')[0]:
                    if element.tag == 'strong':
                        data_type = element.text.strip()[:-1].lower()
                        if data_type == 'radical':
                            kanji_data['meta'][data_type] = (element.tail.strip()[0])
                    elif element.tag == 'a':
                        data_type = element.text.strip().lower()
                        if data_type == 'parts':
                            kanji_data['meta'][data_type].append(element.text)
                        elif data_type == 'variants':
                            kanji_data['meta'][data_type] = tuple(element.text.strip())
                # Parse readings
                type_cache = ''
                for element in kanji_page.cssselect('.readings .japanese_readings')[0]:
                    if element.text:
                        types = ['kun', 'on', 'names']
                        if element.text.startswith('Japanese'):
                            elem = element.text.split(' ')[1][:-1]
                            type_cache = [item for item in types if item == elem][0]
                        if type_cache:
                            if element.tag == 'a':
                                kanji_data['readings'][type_cache].append(element.text)
                            elif element.tag == 'span':
                                if len(element):  # <a> is wrapped into <span>
                                    kanji_data['readings'][type_cache].append(element[0].text)
                                else:
                                    kanji_data['readings'][type_cache].append(element.text)
                # Parse meanings
                meanings = kanji_page.cssselect('.meanings .english_meanings p')[0]
                kanji_data['meanings'].append(meanings.text[:-1])  # append the first meaning
                for element in meanings:
                    if element.tag == 'span':
                        kanji_data['meanings'].append(element.text[:-1])
                    elif element.tag == 'br' and element.tail:
                        kanji_data['meanings'].append(element.tail[:-1])
                response = discord.Embed(color=0xF9F9F9)
                response.set_author(name=f"Jisho.org | {kanji_data['kanji']}", url=search_url, icon_url=jisho_icon)
                response.set_image(url=kanji_data['stroke order'])
                readings = kanji_data['readings']
                readings = '\n'.join(
                    [f"**{reading_type.title()}:** {', '.join(readings[reading_type])}"
                     for reading_type in readings
                     if readings[reading_type]])
                meta = kanji_data['meta']
                response.description = f"**{kanji_data['strokes']}** strokes\n" + '\n'.join([
                    f"**{data_type.capitalize()}:** {', '.join([value for value in meta[data_type]])}"
                    for data_type in meta
                    if meta[data_type]])
                response.description += f"\n**Meanings:** {', '.join(kanji_data['meanings'])}"
                response.add_field(name='Readings', value=readings)
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 No results.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Could not retrieve Jisho data.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted')
    await message.channel.send(None, embed=response)
