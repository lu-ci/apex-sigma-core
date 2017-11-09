import secrets

import aiohttp
import discord
from lxml import html


async def grab_post_list(tags):
    links = []
    for x in range(0, 20):
        resource = f'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags={tags}&pid={x}'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            if 'file_url' in post.attrib:
                file_url = post.attrib['file_url']
                extention = file_url.split('.')[-1]
                if extention in ['png', 'jpg', 'jpeg', 'gif']:
                    height = int(post.attrib['height'])
                    width = int(post.attrib['width'])
                    if width < 2000 and height < 2000:
                        links.append(post)
    return links


def generate_embed(post, titles, color=0xff6699, icon='https://i.imgur.com/WQbzk9y.png'):
    image_url = post.attrib['file_url']
    image_source = f'http://safebooru.org/index.php?page=post&s=view&id={post.attrib["id"]}'
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    embed = discord.Embed(color=color)
    embed.set_author(name=secrets.choice(titles), icon_url=icon, url=image_source)
    embed.set_image(url=image_url)
    embed.set_footer(
        text=f'Score: {post.attrib["score"]} | Size: {post.attrib["width"]}x{post.attrib["height"]}')
    return embed
