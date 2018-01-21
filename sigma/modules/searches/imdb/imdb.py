import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def imdb(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        search = '%20'.join(args)
        api_url = f'http://sg.media-imdb.com/suggests/{search[0].lower()}/{search}.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data:
                search_data = await data.text()
                search_data = '('.join(search_data.split("(")[1:])[:-1]
                data = json.loads(search_data, encoding='utf-8')
        if 'd' in data:
            data = data['d'][0]
            imdb_icon = 'https://ia.media-imdb.com/images/G/01/imdb/images/mobile/'
            imdb_icon += 'apple-touch-icon-web-152x152-1475823641._CB522736557_.png'
            title = data['l']
            staring = data['s']
            if 'y' in data:
                year = data['y']
            else:
                year = 'Unknown'
            image = data['i'][0]
            movie_id = data['id']
            imdb_movie_url = f'http://www.imdb.com/title/{movie_id}/'
            movie_desc = f'IMDB Page: [Here]({imdb_movie_url})'
            movie_desc += f'\nRelease Year: {year}'
            movie_desc += f'\nStaring: {staring}'
            response = discord.Embed(color=0xebc12d)
            response.add_field(name=title, value=movie_desc)
            response.set_thumbnail(url=image)
            response.set_footer(text='From the Internet Movie DataBase.', icon_url=imdb_icon)
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
