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
import lxml.html as lx

from sigma.core.utilities.generic_responses import GenericResponse

lexico_icon = 'https://www.lexico.com/apple-touch-icon.png'


def scrape_gramb(section):
    """
    Scrapes a GRAMB section for definition data.
    :param section: The section to parse.
    :type section: lxml.html.HtmlElement
    :return:
    :rtype: dict
    """
    gramb_type = section[0][0].text
    trgs = section.cssselect('.trg')
    parsed_trgs = []
    ti = 0
    for trg in trgs:
        if len(trg):
            context = trg.cssselect('.ind')[0].text.strip()
            subsenses = []
            subs = trg.cssselect('.subSense')
            si = 0
            for sub in subs:
                sub_context = sub.cssselect('.ind')[0].text.strip()
                sub_data = {
                    'index': si + 1,
                    'context': sub_context
                }
                subsenses.append(sub_data)
                si += 1
            trg_data = {
                'index': ti + 1,
                'context': context,
                'subsenses': subsenses
            }
            parsed_trgs.append(trg_data)
            ti += 1

    data = {
        'type': gramb_type.title() if gramb_type else 'Unknown Type',
        'trgs': parsed_trgs
    }
    return data


def scrape_lexico(page):
    """
    Scrapes the given page for contents.
    :param page: The HTML contents of the page.
    :type page: str
    :return:
    :rtype: dict
    """
    root = lx.fromstring(page)
    try:
        word = root.cssselect('.hwg .hw')[0].text
        sections = root.cssselect('.gramb')
        audio_link = root.cssselect('.headwordAudio')
        audio_link = audio_link[0][0].attrib.get('src') if len(audio_link) else None
        data = {
            'word': word.title(),
            'audio': audio_link,
            'grambs': [scrape_gramb(s) for s in sections if s.attrib.get('class') == 'gramb' and s.tag == 'section']
        }
    except IndexError:
        data = None
    return data


async def dictionary(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        query = '_'.join(pld.args).lower()
        lexico_url = f'https://www.lexico.com/en/definition/{query}'
        async with aiohttp.ClientSession() as session:
            async with session.get(lexico_url) as data_response:
                data = await data_response.text()
                data = scrape_lexico(data)
        if data:
            response = discord.Embed(color=0x50b46c)
            response.set_author(name=f'Lexico Dictionary: {data.get("word")}', icon_url=lexico_icon, url=lexico_url)
            for gramb in data.get('grambs'):
                gramb_lines = []
                for trg in gramb.get('trgs'):
                    gramb_lines.append(f'**{trg.get("index")}.** {trg.get("context")}')
                    for sub in trg.get("subsenses"):
                        gramb_lines.append(f'-> **{trg.get("index")}.{sub.get("index")}.** {sub.get("context")}')
                gramb_text = '\n'.join(gramb_lines[:10])
                if gramb_text:
                    response.add_field(name=gramb.get("type"), value=gramb_text, inline=False)
            if data.get('audio'):
                response.description = f'{data.get("word")} Pronunciation Audio: [Here]({data.get("audio")})'
        else:
            response = GenericResponse('No results.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
