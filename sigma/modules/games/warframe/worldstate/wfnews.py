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
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand


def get_english_message(data):
    message_content = None
    for message in data['Messages']:
        if message['LanguageCode'] == 'en':
            message_content = message
            break
    return message_content


async def wfnews(cmd: SigmaCommand, message: discord.Message, args: list):
    news_url = 'http://content.warframe.com/dynamic/worldState.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(news_url) as data:
            news_data = await data.read()
            news_data = json.loads(news_data)
    news_data = news_data['Events']
    news_lines = []
    for news in reversed(news_data):
        eng_msg = get_english_message(news)
        if eng_msg:
            headline = eng_msg["Message"]
            news_url = news['Prop']
            human_time = arrow.get(int(news['Date']['$date']['$numberLong']) / 1000).humanize()
            news_line = f'[{headline}]({news_url}) - {human_time}'
            news_lines.append(news_line)
    output_text = '\n'.join(news_lines)
    response = discord.Embed(color=0x336699, title='Warframe News')
    response.description = output_text
    await message.channel.send(embed=response)
