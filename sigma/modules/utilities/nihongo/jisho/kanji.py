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
    limit = 1
    jisho_q = ''.join(args)[:limit]

    async with aiohttp.ClientSession() as session:
        async with session.get('http://classic.jisho.org/kanji/details/' + jisho_q) as data:
            rq_text = await data.text()

    if rq_text.find('503 Service Unavailable') != -1:
        embed_content = discord.Embed(title='❗ Jisho responded with 503 Service Unavailable.',
                                      color=0xDB0000)
        await message.channel.send(None, embed=embed_content)
        return

    kanji_data = html.fromstring(rq_text).cssselect('.kanji_result')

    if not kanji_data:
        embed_content = discord.Embed(title='❗ Found 0 kanji',
                                      color=0xDB0000)
        await message.channel.send(None, embed=embed_content)
    else:
        search_url = f'http://jisho.org/search/{jisho_q}%20%23kanji'
        jisho_icon = 'https://i.imgur.com/X1fCJLV.png'
        for kanji_page in kanji_data[:limit]:
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
                data_type = element.text.strip().lower()
                if element.tag == 'strong':
                    data_type = element.text.strip()[:-1].lower()
                    if data_type == 'radical':
                        kanji_data['meta'][data_type] = (element.tail.strip()[0])
                elif element.tag == 'a':
                    if data_type == 'parts':
                        kanji_data['meta'][data_type].append(element.text)
                    elif data_type == 'variants':
                        kanji_data['meta'][data_type] = tuple(element.text.strip())

            # Parse readings
            for element in kanji_page.cssselect('.readings .japanese_readings')[0]:
                reading_type = element.text.split(' ')[1]
                if element.tag == 'strong':
                    reading_type = element.text.split(' ')[1][:-1]  # kun or on
                elif element.tag == 'a':
                    kanji_data['readings'][reading_type].append(element.text)
                elif element.tag == 'span':
                    if len(element):  # <a> is wrapped into <span>
                        kanji_data['readings'][reading_type].append(element[0].text)
                    else:
                        kanji_data['readings'][reading_type].append(element.text)

            # Parse meanings
            meanings = kanji_page.cssselect('.meanings .english_meanings p')[0]
            kanji_data['meanings'].append(meanings.text[:-1])  # append the first meaning
            for element in meanings:
                if element.tag == 'span':
                    kanji_data['meanings'].append(element.text[:-1])
                elif element.tag == 'br' and element.tail:
                    kanji_data['meanings'].append(element.tail[:-1])

            embed = discord.Embed(color=0xF9F9F9)
            embed.set_author(name=f"Jisho.org | {kanji_data['kanji']}", url=search_url, icon_url=jisho_icon)
            embed.set_image(url=kanji_data['stroke order'])

            readings = kanji_data['readings']
            readings = '\n'.join(
                [f"**{reading_type.capitalize()}:** {', '.join(readings[reading_type])}"
                 for reading_type in readings
                 if readings[reading_type]])
            meta = kanji_data['meta']
            embed.description = f"**{kanji_data['strokes']}** strokes\n" + '\n'.join([
                f"**{data_type.capitalize()}:** {', '.join([value for value in meta[data_type]])}"
                for data_type in meta
                if meta[data_type]])
            embed.description += f"\n**Meanings:** {', '.join(kanji_data['meanings'])}"
            embed.add_field(name='Readings', value=readings)
            await message.channel.send(None, embed=embed)
