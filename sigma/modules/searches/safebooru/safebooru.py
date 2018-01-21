from sigma.core.mechanics.command import SigmaCommand
import secrets

import aiohttp
import discord
from lxml import html


async def safebooru(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        tag = 'cute'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    resource = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=' + tag
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
    posts = html.fromstring(data)
    if len(posts) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 Nothing found.')
    else:
        choice = secrets.choice(posts)
        image_url = choice.attrib['file_url']
        icon_url = 'https://i.imgur.com/3Vb6LdJ.png'
        post_url = f'http://safebooru.org/index.php?page=post&s=view&id={choice.attrib["id"]}'
        if image_url.startswith('//'):
            image_url = 'http:' + image_url
        embed = discord.Embed(color=0x8bb2a7)
        embed.set_author(name='Safebooru', icon_url=icon_url, url=post_url)
        embed.set_image(url=image_url)
        embed.set_footer(
            text=f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}')
    await message.channel.send(None, embed=embed)
