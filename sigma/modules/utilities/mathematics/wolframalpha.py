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

import discord
import aiohttp
import lxml.html as lx
from urllib.parse import quote

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.minigames.quiz.mathgame import ongoing_list as math_chs

wolfram_icon = 'https://i.imgur.com/sGKq1A6.png'
wolfram_url = f'http://www.wolframalpha.com/input/?i='
api_url = 'http://api.wolframalpha.com/v2/query?format=plaintext&input='


async def get_url_body(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
    return data


async def get_results(query_url: str):
    results = ''
    if query_url:
        query_page_xml = await get_url_body(query_url)
        if query_page_xml:
            query_page = lx.fromstring(query_page_xml)
            pods = query_page.getchildren()
            if len(pods) >= 2:
                subpods = pods[1].getchildren()
                for subpod in subpods:
                    for element in subpod.getiterator():
                        if element.tag == 'plaintext':
                            if element.text:
                                results += element.text + '\n\n'
    return results


def make_safe_query(query: str):
    query_list = list(query)
    safe_query = ''
    while query_list:
        char = query_list.pop(0)
        safe_query += quote(char, safe='')
    return safe_query


async def send_response(message: discord.Message, init: discord.Message or None, response: discord.Embed):
    await init.edit(embed=response) if init else await message.channel.send(embed=response)


async def wolframalpha(cmd: SigmaCommand, message: discord.Message, args: list):
    api_key = cmd.cfg.get('app_id')
    init_message = None
    if api_key:
        if message.channel.id not in math_chs:
            if args:
                lookup = ' '.join(args).lower()
                query = make_safe_query(lookup)
                url = f'{api_url}{query}&appid={api_key}'
                init_response = discord.Embed(color=0xff7e00)
                init_response.set_author(name='Processing request...', icon_url=wolfram_icon)
                init_message = await message.channel.send(embed=init_response)
                results = await get_results(url)
                if results:
                    if len(results) <= 2000:
                        response = discord.Embed(color=0xff7e00, description=f'```\n{results}\n```')
                        response.set_author(name='Wolfram Alpha', icon_url=wolfram_icon, url=wolfram_url + query)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Results too long to display.')
                        response.description = f'You can view them directly [here]({wolfram_url + query}).'
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 No results.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Wolfram can\'t be used during an ongoing math game.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await send_response(message, init_message, response)
