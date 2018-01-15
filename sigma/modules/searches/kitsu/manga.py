import json

import aiohttp
import discord


async def manga(cmd, message, args):
    if args:
        qry = '%20'.join(args)
        url = f'https://kitsu.io/api/edge/manga?filter[text]={qry}'
        kitsu_icon = 'https://avatars3.githubusercontent.com/u/7648832?v=3&s=200'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        if data['data']:
            ani_url = None
            for result in data['data']:
                for title_key in result.get('attributes').get('titles'):
                    atr_title = result.get('attributes').get('titles').get(title_key)
                    if atr_title:
                        if qry.lower() == atr_title.lower() or atr_title.lower().startswith(qry.lower()):
                            ani_url = result.get('links').get('self')
                            break
            if not ani_url:
                ani_url = data['data'][0]['links']['self']
            async with aiohttp.ClientSession() as session:
                async with session.get(ani_url) as data:
                    data = await data.read()
                    data = json.loads(data)
                    data = data['data']
            attr = data['attributes']
            slug = attr['slug']
            synopsis = attr['synopsis']
            if 'en' in attr['titles']:
                en_title = attr['titles']['en']
            else:
                en_title = attr['titles']['en_jp']
            if 'ja_jp' in attr['titles']:
                jp_title = attr['titles']['ja_jp']
            else:
                jp_title = attr['titles']['en_jp']
            if 'averageRating' in attr:
                rating = attr['averageRating']
                if rating:
                    rating = attr['averageRating'][:5]
                else:
                    rating = 'Unknown'
            else:
                rating = 'Unknown'
            volume_count = attr['volumeCount']
            chapter_count = attr['chapterCount']
            start_date = attr['startDate']
            end_date = attr['endDate']
            age_rating = attr['ageRating']
            anime_desc = f'Title: {jp_title}'
            anime_desc += f'\nRating: {rating}'
            anime_desc += f'\nPublished: {start_date} - {end_date}'
            anime_desc += f'\nVolumes: {volume_count}'
            anime_desc += f'\nChapters: {chapter_count}'
            anime_desc += f'\nAge Rating: {age_rating}'
            response = discord.Embed(color=0xff3300)
            response.set_author(name=f'{en_title or jp_title}', icon_url=kitsu_icon,
                                url=f'https://kitsu.io/manga/{slug}')
            response.add_field(name='Information', value=anime_desc)
            response.add_field(name='Synopsis', value=f'{synopsis[:384]}...')
            if attr['posterImage']:
                poster_image = attr['posterImage']['original'].split('?')[0]
                response.set_thumbnail(url=poster_image)
            response.set_footer(text='Click the title at the top to see the page of the manga.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
