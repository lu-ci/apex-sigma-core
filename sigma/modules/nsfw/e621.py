import json
import secrets

import aiohttp
import discord


async def e621(cmd, message, args):
    url_base = 'https://e621.net/post/index.json'
    if args:
        url = url_base + '?tags=' + '+'.join(args)
    else:
        url = url_base + '?tags=nude'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as data:
            data = await data.read()
            data = json.loads(data)
    if data:
        post = secrets.choice(data)
        image_url = post['file_url']
        icon_url = 'https://e621.net/favicon.ico'
        post_url = f'https://e621.net/post/show/{post["id"]}'
        embed = discord.Embed(color=0x152F56)
        embed.set_author(name='e621', url=post_url, icon_url=icon_url)
        embed.set_image(url=image_url)
        embed.set_footer(text=f'Score: {post["score"]} | Size: {post["width"]}x{post["height"]}')
    else:
        embed = discord.Embed(color=0x696969, title='🔍 Nothing found.')
    await message.channel.send(None, embed=embed)
