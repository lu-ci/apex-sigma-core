import secrets

import aiohttp
import discord
from lxml import html

cache = {}


async def fill_xbooru_cache(tags):
    xbooru_url = f'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}'
    async with aiohttp.ClientSession() as session:
        async with session.get(xbooru_url) as data:
            data = await data.read()
            posts = html.fromstring(data)
            cache.update({tags: list(posts)})


async def xbooru(cmd, message, args):
    global cache
    tags = '+'.join(args)
    if not tags:
        tags = 'nude'
    if tags not in cache:
        collect_needed = True
    else:
        if not cache.get(tags):
            collect_needed = True
        else:
            collect_needed = False
    if collect_needed:
        await fill_xbooru_cache(tags)
    collection = cache.get(tags)
    if collection:
        choice = collection.pop(secrets.randbelow(len(collection)))
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"http:{choice.attrib['file_url']}"
        post_url = f'http://xbooru.com/index.php?page=post&s=view&id={choice.attrib["id"]}'
        icon_url = 'http://xbooru.com/apple-touch-icon-152x152-precomposed.png'
        footer_text = f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}'
        response = discord.Embed(color=0xfede80)
        response.set_author(name='Xbooru', icon_url=icon_url, url=post_url)
        response.set_image(url=img_url)
        response.set_footer(text=footer_text)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 Search yielded no results.')
    await message.channel.send(None, embed=response)
