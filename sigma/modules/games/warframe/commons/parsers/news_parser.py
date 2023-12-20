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

from sigma.modules.games.warframe.commons.worldstate import WorldState


async def get_news_data(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: dict, list
    """
    news_list = await WorldState().news
    news_out = None
    triggers = ['news']
    for news in news_list:
        event_id = news['id']
        db_check = await db[db.db_name].WarframeCache.find_one({'event_id': event_id})
        if not db_check:
            now = arrow.utcnow().int_timestamp
            await db[db.db_name].WarframeCache.insert_one({'event_id': event_id, 'created': now})
            en_trans = news.get('translations', {}).get('en')
            if en_trans:
                news_out = news
                triggers += [piece.lower() for piece in en_trans.lower().split()]
                break
    return news_out, triggers


def generate_news_embed(data):
    """
    :type data: dict
    :rtype: discord.Embed
    """
    event_datetime = arrow.get(data['date']).datetime
    en_trans = data['translations']['en']
    response = discord.Embed(color=0x336699, title=en_trans, timestamp=event_datetime, url=data['link'])
    if data.get('imageLink'):
        response.set_image(url=data['imageLink'])
    return response
