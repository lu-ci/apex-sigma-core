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
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    api_document = await cmd.db[cmd.db.db_cfg.database]['WaniKani'].find_one({'UserID': target.id})
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

            level = '**Level {}** Apprentice'.format(level)
            avatar = f'https://www.gravatar.com/avatar/{avatar}.jpg?s=300&d='
            avatar += 'https://cdn.wanikani.com/default-avatar-300x300-20121121.png'
            creation_date = arrow.get(creation_date).format('MMMM DD, YYYY')

            radicals = 'Radicals: **{}**/**{}**'.format(radicals_progress, radicals_total)
            kanji = 'Kanji: **{}**/**{}**'.format(kanji_progress, kanji_total)

            embed = discord.Embed(color=target.color)

            level_progression = level + '\n'
            level_progression += radicals + '\n'
            level_progression += kanji
            embed.add_field(name='Level progression', value=level_progression)

            srs_distibution = 'Apprentice: **{}**\n'.format(apprentice)
            srs_distibution += 'Guru: **{}**\n'.format(guru)
            srs_distibution += 'Master: **{}**\n'.format(master)
            srs_distibution += 'Enlighten: **{}**\n'.format(enlighten)
            srs_distibution += 'Burned: **{}**'.format(burned)
            embed.add_field(name='SRS distribution', value=srs_distibution)

            study_queue = 'Lessons available: **{}**\n'.format(lessons_available)
            study_queue += 'Reviews available: **{}**\n'.format(reviews_available)
            if lessons_available or reviews_available:
                next_review = 'now'
            else:
                next_review = arrow.get(next_review).humanize()
            study_queue += 'Next review date: **{}**\n'.format(next_review)
            study_queue += 'Reviews in next hour: **{}**\n'.format(reviews_available_next_hour)
            study_queue += 'Reviews in next day: **{}**'.format(reviews_available_next_day)
            embed.add_field(name='Study queue', value=study_queue)

            userinfo = '**{}** of **Sect {}**\n'.format(username, sect)
            userinfo += '**Level {}** Apprentice\n'.format(level)
            userinfo += 'Serving the Crabigator since {}'.format(creation_date)

            embed.set_author(name='{} of Sect {}'.format(username, sect),
                             url='https://www.wanikani.com/community/people/{}'.format(username), icon_url=avatar)
            embed.set_footer(text='Serving the Crabigator since {}'.format(creation_date))
        except KeyError:
            embed = discord.Embed(color=0xBE1931, title='❗ Invalid data was retrieved.')
    else:
        embed = discord.Embed(color=0xBE1931, title='❗ User has no Key saved.')
    await message.channel.send(None, embed=embed)
