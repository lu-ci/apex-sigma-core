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

import json

import aiohttp
import discord

from sigma.core.utilities.generic_responses import error, not_found

api_base = 'https://en.wikipedia.org/w/api.php?format=json'
wiki_icon = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'


def shorten_sentences(text):
    """
    Transforms a multiline string into a single
    line string of a specified length.
    :param text: The text to parse.
    :type text: str
    :return:
    :rtype: str
    """
    sentences = text.replace('\n', ' ')
    if len(sentences) > 1900:
        sentences = sentences[:1900].rpartition('.')[0] + '...'
    return sentences


def get_exact_results(search_data: list):
    """
    Gets the first exact result from the api response.
    :param search_data: The api response to parse
    :type search_data: dict
    :return:
    :rtype: str, str
    """
    exact_result = None
    search, results, descs, urls = search_data
    for i, result in enumerate(results):
        if not descs[i].endswith('may refer to:'):
            if 'usually refers to' not in descs[i]:
                exact_result = result, urls[i]
                break
    return exact_result


async def wikipedia(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        api_url = f'{api_base}&action=opensearch&search={" ".join(pld.args)}&redirects=resolve'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as qs_session:
                resp_data = await qs_session.read()
                search_data = json.loads(resp_data)
        if search_data[1]:
            exact_result = get_exact_results(search_data)
            if exact_result:
                lookup, wiki_url = exact_result
                summary_url = f'{api_base}&action=query&prop=extracts&exintro&explaintext&titles={lookup}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(summary_url) as qs_session:
                        summ_res_data = await qs_session.read()
                        summ_data = json.loads(summ_res_data)
                pages = summ_data.get('query', {}).get('pages', {})
                page_id = list(pages.keys())[0]
                summ = pages.get(page_id)
                summ_title = summ.get('title')
                summ_content = summ.get('extract')
                if len(summ_content) > 1900:
                    summ_content = shorten_sentences(summ_content)
                response = discord.Embed(color=0xF9F9F9)
                response.set_author(name=summ_title, icon_url=wiki_icon, url=wiki_url)
                response.description = summ_content
            else:
                response = error('Search too broad, please be more specific.')
        else:
            response = not_found('No results.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
