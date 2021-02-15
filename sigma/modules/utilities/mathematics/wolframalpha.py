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

from urllib.parse import quote as escape

import aiohttp
import discord
import lxml.html as lx

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

wolfram_icon = 'https://i.imgur.com/sGKq1A6.png'
wolfram_url = 'http://www.wolframalpha.com/input/?i='
api_url = 'http://api.wolframalpha.com/v2/query?format=plaintext&podindex=2&input='


async def get_url_body(url):
    """
    Asynchronously fetches a URL.
    :type url: str
    :rtype: bytes
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
    return data


async def get_results(query_url):
    """
    Parses the XML response from 'query_url'.
    :type query_url: str
    :rtype: str
    """
    results = ''
    query_page_xml = await get_url_body(query_url)
    if query_page_xml:
        query_page = lx.fromstring(query_page_xml)
        pod_data = query_page.cssselect('queryresult > pod[title] > subpod > plaintext')
        if pod_data:
            results += '\n\n'.join([elem.text_content().strip() for elem in pod_data if elem.text_content().strip()])
    return results


def make_safe_query(query):
    """
    Creates a URL safe string by escaping reserved characters.
    :type query: list[str]
    :rtype: str
    """
    safe = r'`~!@$^*()[]{}\|:;"\'<>,.'
    query_list = list(' '.join(query))
    safe_query = ''
    while query_list:
        char = query_list.pop(0).lower()
        safe_query += escape(char, safe=safe)
    return safe_query


async def send_response(message, init, response):
    """
    Edits the initial command response to display the results.
    Sends a new message if 'init' or if the original isn't found.
    :type message: discord.Message
    :type init: discord.Message or None
    :type response: discord.Embed
    """
    await init.edit(embed=response) if init else await message.channel.send(embed=response)


async def wolframalpha(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    init_message = None
    if cmd.cfg.app_id:
        if not Ongoing.is_ongoing('mathgame', pld.msg.channel.id):
            if pld.args:
                query = make_safe_query(pld.args)
                url = f'{api_url}{query}&appid={cmd.cfg.app_id}'
                init_response = discord.Embed(color=0xff7e00)
                init_response.set_author(name='Processing request...', icon_url=wolfram_icon)
                init_message = await pld.msg.channel.send(embed=init_response)
                results = await get_results(url)
                if results:
                    if len(results) <= 2000:
                        response = discord.Embed(color=0xff7e00, description=f'```\n{results}\n```')
                        response.set_author(name='Wolfram Alpha', icon_url=wolfram_icon, url=wolfram_url + query)
                        response.set_footer(text='View the full results by clicking the embed title.')
                    else:
                        response = GenericResponse('Results too long to display.').error()
                        response.description = f'You can view them directly [here]({wolfram_url + query}).'
                else:
                    response = GenericResponse('No results.').not_found()
            else:
                response = GenericResponse('Nothing inputted.').error()
        else:
            response = GenericResponse('Wolfram can\'t be used during an ongoing math game.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await send_response(pld.msg, init_message, response)
