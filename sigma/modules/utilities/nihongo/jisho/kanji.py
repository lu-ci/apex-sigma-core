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
from lxml import html

from sigma.core.utilities.generic_responses import error, not_found


def make_kanji_dict(kanji_page):
    """

    :param kanji_page:
    :type kanji_page:
    :return:
    :rtype:
    """
    stroke_source = kanji_page.cssselect('.stroke_diagram img')[0].attrib.get('src')
    kanji_dict = {
        'kanji': kanji_page.cssselect('.literal.japanese')[0].text.strip(),
        'strokes': kanji_page.cssselect('.specs strong')[0].text,
        'stroke order': f'http://classic.jisho.org{stroke_source}',
        'meta': {'radical': None, 'parts': [], 'variants': []},
        'readings': {'kun': [], 'on': [], 'names': []},
        'meanings': []
    }
    return kanji_dict


def parse_radical_data(kanji_data, kanji_page):
    """

    :param kanji_data:
    :type kanji_data:
    :param kanji_page:
    :type kanji_page:
    """
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


def parse_readings_data(kanji_data, kanji_page):
    """

    :param kanji_data:
    :type kanji_data:
    :param kanji_page:
    :type kanji_page:
    """
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
                if element.tag == 'span':
                    if len(element):  # <a> is wrapped into <span>
                        kanji_data['readings'][type_cache].append(element[0].text)
                    else:
                        kanji_data['readings'][type_cache].append(element.text)
                if element.tail:
                    kanji_data['readings'][type_cache].append(element.tail)
        elif element.tag == 'span' and len(element) and type_cache:
            kanji_data['readings'][type_cache].append(element[0].text)


def parse_meanings_data(kanji_data, kanji_page):
    """

    :param kanji_data:
    :type kanji_data:
    :param kanji_page:
    :type kanji_page:
    """
    meanings = kanji_page.cssselect('.meanings .english_meanings p')[0]
    kanji_data['meanings'].append(meanings.text[:-1])  # append the first meaning
    for element in meanings:
        if element.tag == 'span':
            kanji_data['meanings'].append(element.text[:-1])
        elif element.tag == 'br' and element.tail:
            kanji_data['meanings'].append(element.tail[:-1])


def clean_readings_data(kanji_dict):
    """

    :param kanji_dict:
    :type kanji_dict:
    :return:
    :rtype:
    """
    readings = kanji_dict['readings']
    bad_chars = ['、 ', '、', '\t', ' ']
    rds = {'readings': {'kun': [], 'on': [], 'names': []}}
    for r_type in readings:
        for item in readings[r_type]:
            if item not in bad_chars:
                for char in bad_chars:
                    if char in item:
                        item = item.replace(char, '')
                rds['readings'][r_type].append(item)
    return rds


async def kanji(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        query = pld.args[0][0]
        async with aiohttp.ClientSession() as session:
            async with session.get('http://classic.jisho.org/kanji/details/' + query) as data:
                rq_text = await data.text()
        if not rq_text.find('503 Service Unavailable') != -1:
            kanji_data = html.fromstring(rq_text).cssselect('.kanji_result')
            if kanji_data:
                kanji_dict = make_kanji_dict(kanji_data[0])
                parse_radical_data(kanji_dict, kanji_data[0])
                parse_readings_data(kanji_dict, kanji_data[0])
                parse_meanings_data(kanji_dict, kanji_data[0])
                readings = clean_readings_data(kanji_dict)['readings']
                rds = [f"**{r_type.title()}:** {', '.join(readings[r_type])}" for r_type in readings if
                       readings[r_type]]
                meta = kanji_dict['meta']
                data = []
                for item in meta:
                    if item:
                        meta_title = f'**{item.title()}:**'
                        meta_list = ', '.join([v for v in meta[item]])
                        data.append(f'{meta_title} {meta_list}')
                desc = f"**{kanji_dict['strokes']}** strokes\n"
                desc += '\n'.join(data)
                desc += f"\n**Meanings:** {', '.join(kanji_dict['meanings'])}"
                search_url = f'http://jisho.org/search/{query}%20%23kanji'
                jisho_icon = 'https://i.imgur.com/X1fCJLV.png'
                response = discord.Embed(color=0xF9F9F9, description=desc)
                response.set_author(name=f"Jisho.org | {kanji_dict['kanji']}", url=search_url, icon_url=jisho_icon)
                response.set_image(url=kanji_dict['stroke order'])
                response.add_field(name='Readings', value='\n'.join(rds))
            else:
                response = not_found('No results.')
        else:
            response = error('Could not retrieve Jisho data.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
