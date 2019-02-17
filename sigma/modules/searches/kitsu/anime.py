# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
from sigma.core.utilities.generic_responses import error, not_found


async def anime(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        qry = '%20'.join(pld.args)
        url = f'https://kitsu.io/api/edge/anime?filter[text]={qry}'
        kitsu_icon = 'https://avatars3.githubusercontent.com/u/7648832?v=3&s=200'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                data = await data.read()
                data = json.loads(data)
        if data.get('data'):
            ani_url = None
            for result in data.get('data'):
                for title_key in result.get('attributes').get('titles'):
                    atr_title = result.get('attributes').get('titles').get(title_key)
                    if atr_title:
                        if qry.lower() == atr_title.lower() or atr_title.lower().startswith(qry.lower()):
                            ani_url = result.get('links').get('self')
                            break
            if not ani_url:
                ani_url = data.get('data')[0].get('links').get('self')
            async with aiohttp.ClientSession() as session:
                async with session.get(ani_url) as data:
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
            episode_count = attr.get('episodeCount') or 0
            episode_length = attr.get('episodeLength')
            start_date = attr.get('startDate') or 'Unknown'
            end_date = attr.get('endDate') or 'Unknown'
            anime_desc = f'Title: {jp_title}'
            anime_desc += f'\nRating: {rating}%'
            anime_desc += f'\nAir Time: {start_date} - {end_date}'
            anime_desc += f'\nEpisodes: {episode_count}'
            if episode_length:
                anime_desc += f'\nDuration: {episode_length} Minutes'
            else:
                anime_desc += '\nDuration: Unknown'
            kitsu_url = f'https://kitsu.io/anime/{slug}'
            response = discord.Embed(color=0xff3300)
            response.set_author(name=f'{en_title or jp_title}', icon_url=kitsu_icon, url=kitsu_url)
            response.add_field(name='Information', value=anime_desc)
            response.add_field(name='Synopsis', value=f'{synopsis[:384]}...')
            if attr.get('posterImage'):
                poster_image = attr.get('posterImage').get('original').split('?')[0]
                response.set_thumbnail(url=poster_image)
            response.set_footer(text='Click the title at the top to see the page of the anime.')
        else:
            response = not_found('No results.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
