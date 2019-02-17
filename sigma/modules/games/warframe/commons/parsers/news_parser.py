# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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


def language_check(data):
    english = False
    for message in data['Messages']:
        if message['LanguageCode'] == 'en':
            english = True
            break
    return english


async def get_news_data(db):
    news_url = 'http://content.warframe.com/dynamic/worldState.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(news_url) as data:
            news_data = await data.read()
            news_data = json.loads(news_data)
    news_data = news_data['Events']
    news_out = None
    triggers = ['news']
    for news in news_data:
        event_id = news['_id']['$oid']
        db_check = await db[db.db_nam].WarframeCache.find_one({'event_id': event_id})
        if not db_check:
            now = arrow.utcnow().timestamp
            await db[db.db_nam].WarframeCache.insert_one({'event_id': event_id, 'created': now})
            if language_check(news):
                news_out = news
                en_news = discord.utils.find(lambda n: n.get('LanguageCode') == 'en', news.get('Messages'))
                triggers += [piece.lower() for piece in en_news.get('Message').lower().split()]
                break
    return news_out, triggers


def generate_news_embed(data):
    event_datetime = arrow.get().utcfromtimestamp(int(data['Date']['$date']['$numberLong']) // 1000).datetime
    message_content = None
    for message in data['Messages']:
        if message['LanguageCode'] == 'en':
            message_content = message
            break
    headline = message_content['Message']
    news_url = data['Prop']
    response = discord.Embed(color=0x336699, title=headline, timestamp=event_datetime, url=news_url)
    if data.get('ImageUrl'):
        response.set_image(url=data['ImageUrl'])
    return response
