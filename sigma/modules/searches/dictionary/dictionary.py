﻿"""
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

LEXICO_ICON = 'https://www.lexico.com/apple-touch-icon.png'


def scrape_gramb(section):
    """
    Scrapes a GRAMB section for definition data.
    :type section: lxml.html.HtmlElement
    :rtype: dict
    """
    gramb_type = section[0][0].text
    trgs = section.cssselect('.trg')
    parsed_trgs = []
    for ti, trg in enumerate(trgs):
        if len(trg):
            context = trg.cssselect('.ind')
            if not context:
                continue
            context = context[0].text.strip()
            subs = trg.cssselect('.subSense .ind')
            cross_ref = trg.cssselect('.crossReference')
            if cross_ref:
                cross_ref = cross_ref[0].text + cross_ref[0][0].text.strip()
                subs.append(cross_ref)

            subsenses = []
            for si, sub in enumerate(subs):
                if not isinstance(sub, str):
                    sub = sub.text.strip()
                sub_data = {
                    'index': si + 1,
                    'context': sub
                }
                subsenses.append(sub_data)
            trg_data = {
                'index': ti + 1,
                'context': context,
                'subsenses': subsenses
            }
            parsed_trgs.append(trg_data)

    data = {
        'type': gramb_type.title() if gramb_type else 'Unknown Type',
        'trgs': parsed_trgs
    }
    return data


def scrape_lexico(page):
    """
    Scrapes the given page for contents.
    :type page: str
    :rtype: dict
    """
    root = lx.fromstring(page)
    try:
        word = root.cssselect('.hwg .hw')[0].text
        sections = root.cssselect('.gramb')
        audio_link = root.cssselect('.pronunciations .speaker audio')
        audio_link = audio_link[0].attrib.get('src') if audio_link else None
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
        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(lexico_url) as data_response:
                body = await data_response.text()
        if body:
            data = scrape_lexico(body)
            if data:
                response = discord.Embed(color=0x50b46c)
                response.set_author(name=f'Lexico Dictionary: {data.get("word")}', icon_url=LEXICO_ICON, url=lexico_url)
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
            response = GenericResponse('The request returned an empty body.').error()
            response.description = 'This usually means there are no results, or something went wrong.'
            response.description += ' Another option is that your word is not correctly written.'
            response.description += ' Like writing "yoyo" instead of "yo-yo", Lexico is strict like that.'
            response.description += f' [Here]({lexico_url}) is a link to your query, it might help.'
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
