import json
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def konachan(cmd: SigmaCommand, message: discord.Message, args: list):
    url_base = 'https://konachan.com/post.json?limit=100&tags='
    if not args:
        tags = 'nude'
    else:
        tags = '+'.join(args)
    url = url_base + tags
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.read()
            data = json.loads(data)
    if len(data) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        post = secrets.choice(data)
        post_url = f'http://konachan.com/post/show/{post["id"]}'
        icon_url = 'https://i.imgur.com/qc4awFL.png'
        embed = discord.Embed(color=0x473a47)
        embed.set_author(name='Konachan', url=post_url, icon_url=icon_url)
        embed.set_image(url=post["file_url"])
        embed.set_footer(
            text=f'Score: {post["score"]} | Size: {post["width"]}x{post["height"]} | Uploaded By: {post["author"]}')
    await message.channel.send(None, embed=embed)
