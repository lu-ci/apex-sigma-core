import secrets

import aiohttp
import discord
from lxml import html


async def cyanideandhappiness(cmd: SigmaCommand, message: discord.Message, args: list):
    comic_img_url = None
    comic_url = None
    while not comic_img_url:
        comic_number = secrets.randbelow(4665) + 1
        comic_url = f'http://explosm.net/comics/{comic_number}/'
        async with aiohttp.ClientSession() as session:
            async with session.get(comic_url) as data:
                page = await data.text()
        root = html.fromstring(page)
        comic_element = root.cssselect('#main-comic')
        comic_img_url = comic_element[0].attrib['src']
        if comic_img_url.startswith('//'):
            comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0xFF6600)
    embed.set_image(url=comic_img_url)
    cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'
    embed.set_author(name='Cyanide and Happiness', icon_url=cnh_image, url=comic_url)
    await message.channel.send(None, embed=embed)
