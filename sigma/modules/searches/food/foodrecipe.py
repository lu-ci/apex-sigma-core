import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def foodrecipe(cmd: SigmaCommand, message: discord.Message, args: list):
    if 'api_key' in cmd.cfg:
        api_key = cmd.cfg['api_key']
        if args:
            search = ' '.join(args)
            url = f'http://food2fork.com/api/search?key={api_key}&q={search}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data:
                    search_data = await data.read()
                    search_data = json.loads(search_data)
            count = search_data['count']
            if count == 0:
                response = discord.Embed(color=0x696969, title='🔍 No results were found for that, sorry.')
            else:
                info = search_data['recipes'][0]
                title = info['title']
                source = info['publisher']
                source_url = info['source_url']
                image_url = info['image_url']
                publisher_url = info['publisher_url']
                response = discord.Embed(color=0xee5b2f)
                response.set_author(name=source, url=publisher_url, icon_url='https://i.imgur.com/RH8LNdQ.png')
                response.add_field(name=title, value='[Recipe Here](' + source_url + ')')
                response.set_thumbnail(url=image_url)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(None, embed=response)
