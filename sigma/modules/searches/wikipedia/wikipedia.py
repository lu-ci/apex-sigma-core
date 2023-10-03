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

import arrow
import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget

api_base = 'https://en.wikipedia.org/w/api.php?format=json'
wiki_icon = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'
stat_base = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/'


def shorten_sentences(text):
    """
    Transforms a multiline string into a single
    line string of a specified length.
    :type text: str
    :rtype: str
    """
    sentences = text.replace('\n', '\n\n')
    if len(sentences) > 4000:
        sentences = sentences[:4000].rpartition('.')[0] + '...'
    return sentences


def get_exact_results(search_data):
    """
    Gets the first exact result from the api response.
    :type search_data: dict
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
        search_data = await aioget(api_url, as_json=True)

        if search_data[1]:
            exact_result = get_exact_results(search_data)
            if exact_result:
                lookup, wiki_url = exact_result
                summary_url = f'{api_base}&action=query&prop=extracts&exintro&explaintext&titles={lookup}'
                summ_data = await aioget(summary_url, as_json=True)

                pages = summ_data.get('query', {}).get('pages', {})
                page_id = list(pages.keys())[0]
                summ = pages.get(page_id)
                summ_title = summ.get('title')
                summ_content = summ.get('extract')
                summ_content = shorten_sentences(summ_content)

                now = arrow.utcnow()
                stat_start = now.shift(days=-60).format('YYYYMMDDHH')
                stat_end = now.format('YYYYMMDDHH')
                page_stats = await aioget(f'{stat_base}{lookup}/monthly/{stat_start}/{stat_end}', True)
                page_views = page_stats.get('items', [{}])[0].get('views', 0)

                response = discord.Embed(color=0xF9F9F9)
                response.set_author(name=summ_title, icon_url=wiki_icon, url=wiki_url)
                response.description = summ_content
                response.set_footer(text=f'{page_views} people viewed this article in the last month')
            else:
                response = GenericResponse('Search too broad, please be more specific.').error()
        else:
            response = GenericResponse('No results.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
