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
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand


async def wanikani(cmd: SigmaCommand, message: discord.Message, args: list):
    target = message.mentions[0] if message.mentions else message.author
    api_document = await cmd.db[cmd.db.db_nam]['WaniKani'].find_one({'UserID': target.id})
    if api_document:
        try:
            api_key = api_document['WKAPIKey']
            url = f'https://www.wanikani.com/api/user/{api_key}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/srs-distribution') as data:
                    srs = await data.read()
                    srs = json.loads(srs)
                    username = srs['user_information']['username']
                    sect = srs['user_information']['title']
                    level = srs['user_information']['level']
                    avatar = srs['user_information']['gravatar']
                    creation_date = srs['user_information']['creation_date']
                    apprentice = srs['requested_information']['apprentice']['total']
                    guru = srs['requested_information']['guru']['total']
                    master = srs['requested_information']['master']['total']
                    enlighten = srs['requested_information']['enlighten']['total']
                    burned = srs['requested_information']['burned']['total']
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/study-queue') as data:
                    study = await data.read()
                    study = json.loads(study)
                    lessons_available = study['requested_information']['lessons_available']
                    reviews_available = study['requested_information']['reviews_available']
                    next_review = study['requested_information']['next_review_date']
                    reviews_available_next_hour = study['requested_information']['reviews_available_next_hour']
                    reviews_available_next_day = study['requested_information']['reviews_available_next_day']
            async with aiohttp.ClientSession() as session:
                async with session.get(url + '/level-progression') as data:
                    progression = await data.read()
                    progression = json.loads(progression)
                    radicals_progress = progression['requested_information']['radicals_progress']
                    radicals_total = progression['requested_information']['radicals_total']
                    kanji_progress = progression['requested_information']['kanji_progress']
                    kanji_total = progression['requested_information']['kanji_total']
            level = f'**Level {level}** Apprentice'
            avatar = f'https://www.gravatar.com/avatar/{avatar}.jpg?s=300&d='
            avatar += 'https://cdn.wanikani.com/default-avatar-300x300-20121121.png'
            creation_date = arrow.get(creation_date).format('MMMM DD, YYYY')
            radicals = f'Radicals: **{radicals_progress}**/**{radicals_total}**'
            kanji = f'Kanji: **{kanji_progress}**/**{kanji_total}**'
            response = discord.Embed(color=target.color)
            level_progression = level + '\n'
            level_progression += radicals + '\n'
            level_progression += kanji
            response.add_field(name='Level progression', value=level_progression)
            srs_distibution = f'Apprentice: **{apprentice}**\n'
            srs_distibution += f'Guru: **{guru}**\n'
            srs_distibution += f'Master: **{master}**\n'
            srs_distibution += f'Enlighten: **{enlighten}**\n'
            srs_distibution += f'Burned: **{burned}**'
            response.add_field(name='SRS distribution', value=srs_distibution)
            study_queue = f'Lessons available: **{lessons_available}**\n'
            study_queue += f'Reviews available: **{reviews_available}**\n'
            if lessons_available or reviews_available:
                next_review = 'now'
            else:
                next_review = arrow.get(next_review).humanize()
            study_queue += f'Next review date: **{next_review}**\n'
            study_queue += f'Reviews in next hour: **{reviews_available_next_hour}**\n'
            study_queue += f'Reviews in next day: **{reviews_available_next_day}**'
            response.add_field(name='Study queue', value=study_queue)
            userinfo = f'**{username}** of **Sect {sect}**\n'
            userinfo += f'**Level {level}** Apprentice\n'
            userinfo += f'Serving the Crabigator since {creation_date}'
            response.set_author(name=f'{username} of Sect {sect}',
                                url=f'https://www.wanikani.com/community/people/{username}', icon_url=avatar)
            response.set_footer(text=f'Serving the Crabigator since {creation_date}')
        except KeyError:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid data was retrieved.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ User has no Key saved.')
    await message.channel.send(embed=response)
