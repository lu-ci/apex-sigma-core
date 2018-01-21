import json

import aiohttp
import arrow
import discord


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
