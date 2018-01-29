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
    for news in news_data:
        event_id = news['_id']['$oid']
        db_check = await db[db.db_cfg.database]['WarframeCache'].find_one({'EventID': event_id})
        if not db_check:
            await db[db.db_cfg.database]['WarframeCache'].insert_one({'EventID': event_id})
            if language_check(news):
                news_out = news
                break
    return news_out


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
