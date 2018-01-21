import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def randomcomicgenerator(cmd: SigmaCommand, message: discord.Message, args: list):
    comic_url = 'http://explosm.net/rcg/'
    async with aiohttp.ClientSession(cookies={'explosm': 'nui4hbhpq55tr4ouqknb060jr4'}) as session:
        async with session.get(comic_url) as data:
            page = await data.text()
    root = html.fromstring(page)
    comic_element = root.cssselect('#rcg-comic')
    comic_img_url = comic_element[0][0].attrib['src']
    if comic_img_url.startswith('//'):
        comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0xFF6600)
    cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'
    embed.set_author(name='Cyanide and Happiness Random Comic Generator', icon_url=cnh_image, url=comic_url)
    embed.set_image(url=comic_img_url)
    await message.channel.send(None, embed=embed)
