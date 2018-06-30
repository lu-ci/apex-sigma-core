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
import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand

api_base = 'https://en.wikipedia.org/w/api.php?format=json'
wiki_icon = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Wikipedia_logo_silver.png'


def shorten_sentences(text: str):
    sentences = [f'{s.strip()}.' for s in text.replace('\n', ' ').split('.')]
    new_sentences = []
    for sentence in sentences:
        if len(' '.join(new_sentences)) + len(sentence) < 1900:
            new_sentences.append(sentence)
        else:
            break
    return f'{" ".join(new_sentences)}...'


async def wikipedia(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        api_url = f'{api_base}&action=opensearch&search={" ".join(args)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as qs_session:
                resp_data = await qs_session.read()
                search_data = json.loads(resp_data)
        results = search_data[1]
        if results:
            descriptions = search_data[2]
            articles = search_data[3]
            exact_result = None
            for result in enumerate(results):
                index = result[0]
                if not descriptions[index].endswith('may refer to:'):
                    exact_result = results[index], articles[index]
                    break
            if exact_result:
                lup, url = exact_result
                summary_url = f'{api_base}&action=query&prop=extracts&exintro&explaintext&titles={lup}'
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
                response.set_author(name=summ_title, icon_url=wiki_icon, url=url)
                response.description = summ_content
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Search too broad, please be more specific.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
