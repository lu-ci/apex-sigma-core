from sigma.core.mechanics.command import SigmaCommand
import datetime
import json
import secrets

import aiohttp
import discord


async def deezer(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        search = '%20'.join(args)
        qry_url = f'http://api.deezer.com/search/track?q={search}'
        async with aiohttp.ClientSession() as session:
            async with session.get(qry_url) as data:
                data = await data.read()
                data = json.loads(data)
                data = data['data']
        if data:
            data = data[0]
            track_url = data['link']
            track_title = data['title_short']
            track_duration = data['duration']
            preview_url = data['preview']
            artist_name = data['artist']['name']
            artist_image = data['artist']['picture_medium']
            album_title = data['album']['title']
            album_image = data['album']['cover_medium']
            deezer_icon = 'http://e-cdn-files.deezer.com/images/common/favicon/favicon-96x96-v00400045.png'
            deezer_colors = [0xff0000, 0xffed00, 0xff0092, 0xbed62f, 0x00c7f2]
            deezer_color = secrets.choice(deezer_colors)
            song_desc = f'Preview: [Here]({preview_url})'
            song_desc += f'\nDuration: {datetime.timedelta(seconds=track_duration)}'
            response = discord.Embed(color=deezer_color)
            response.set_author(name=artist_name, icon_url=artist_image, url=track_url)
            response.add_field(name=f'{track_title}', value=song_desc)
            response.set_thumbnail(url=album_image)
            response.set_footer(icon_url=deezer_icon, text=f'Album: {album_title}')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
