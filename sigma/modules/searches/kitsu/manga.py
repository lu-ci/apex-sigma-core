# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def manga(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        qry = '%20'.join(pld.args)
        url = f'https://kitsu.io/api/edge/manga?filter[text]={qry}'
        kitsu_icon = 'https://avatars3.githubusercontent.com/u/7648832?v=3&s=200'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        if data.get('data'):
            man_url = None
            for result in data.get('data'):
                for title_key in result.get('attributes').get('titles'):
                    atr_title = result.get('attributes').get('titles').get(title_key)
                    if atr_title:
                        if qry.lower() == atr_title.lower() or atr_title.lower().startswith(qry.lower()):
                            man_url = result.get('links').get('self')
                            break
            if not man_url:
                man_url = data.get('data')[0].get('links').get('self')
            async with aiohttp.ClientSession() as session:
                async with session.get(man_url) as data:
                    data = await data.read()
                    data = json.loads(data)
                    data = data.get('data')
            attr = data.get('attributes')
            slug = attr.get('slug')
            synopsis = attr.get('synopsis')
            en_title = attr.get('titles').get('en') or attr.get('titles').get('en_jp')
            jp_title = attr.get('titles').get('ja_jp') or attr.get('titles').get('en_jp')
            rating = attr.get('averageRating')
            if rating:
                rating = attr.get('averageRating')[:5]
            else:
                rating = '?'
            volume_count = attr.get('volumeCount') or '?'
            chapter_count = attr.get('chapterCount') or '?'
            start_date = attr.get('startDate') or 'Unknown'
            end_date = attr.get('endDate') or 'Unknown'
            age_rating = attr.get('ageRating') or 'Unknown'
            manga_desc = f'Title: {jp_title}'
            manga_desc += f'\nRating: {rating}'
            manga_desc += f'\nPublished: {start_date} - {end_date}'
            manga_desc += f'\nVolumes: {volume_count}'
            manga_desc += f'\nChapters: {chapter_count}'
            manga_desc += f'\nAge Rating: {age_rating}'
            kitsu_url = f'https://kitsu.io/manga/{slug}'
            response = discord.Embed(color=0xff3300)
            response.set_author(name=f'{en_title or jp_title}', icon_url=kitsu_icon, url=kitsu_url)
            response.add_field(name='Information', value=manga_desc)
            response.add_field(name='Synopsis', value=f'{synopsis[:384]}...')
            if attr.get('posterImage'):
                poster_image = attr.get('posterImage').get('original').split('?')[0]
                response.set_thumbnail(url=poster_image)
            response.set_footer(text='Click the title at the top to see the page of the manga.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No results.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
