import json
import secrets
from sigma.core.mechanics.command import SigmaCommand

import aiohttp
import discord
import ftfy
from lxml import html


async def joke(cmd: SigmaCommand, message: discord.Message, args: list):
    randomizer = secrets.randbelow(6644)
    joke_url = f'http://jokes.cc.com/feeds/random/{randomizer}'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.read()
            joke_json = json.loads(joke_json)
            joke_page_url = joke_json['0']['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_page_url) as data:
            page_data = await data.text()
    root = html.fromstring(page_data)
    content = root.cssselect('.content_wrap')[0]
    joke_text = ''
    for element in content.cssselect('p'):
        if element.text != '' and element.text != '\n':
            joke_text += f'\n{element.text}'
    while '  ' in joke_text:
        joke_text = joke_text.replace('  ', ' ')
    joke_text = ftfy.fix_text(joke_text)
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😆 Have A Random Joke', value=joke_text)
    await message.channel.send(None, embed=embed)
