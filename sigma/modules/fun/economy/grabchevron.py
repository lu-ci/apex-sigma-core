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
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.modules.core_functions.chevron.spawn_chevron import chev_cache


async def interact_chevron(db: Database, author: discord.Member, good: bool, attrib: str, act: str):
    profile = await db[db.db_nam].Profiles.find_one({'user_id': author.id})
    if not profile:
        await db[db.db_nam].Profiles.insert_one({'user_id': author.id})
        profile = {}
    chevron_data = profile.get('chevrons', {})
    chevron_list = chevron_data.get('items', [])
    chevron_tally = chevron_data.get('total', 0)
    chevron_list.append(
        {
            'server_id': author.guild.id, 'type': attrib,
            'time': arrow.utcnow().timestamp, 'good': good, 'act': act
        }
    )
    if good:
        chevron_tally += 1
    else:
        chevron_tally = round(chevron_tally / 2)
    chevron_data.update({'items': chevron_list, 'total': chevron_tally})
    profile.update({'chevrons': chevron_data})
    await db[db.db_nam].Profiles.update_one({'user_id': author.id}, {'$set': profile})


async def grabchevron(cmd: SigmaCommand, message: discord.Message, args: list):
    chev_data = chev_cache.get_cache(message.channel.id) if message.guild else None
    if chev_data:
        chev_good, chev_attrib = chev_data
        if args:
            chev_look = ' '.join(args).lower()
            if chev_look.lower() == chev_attrib.lower():
                chev_cache.del_cache(message.channel.id)
                await interact_chevron(cmd.db, message.author, chev_good, chev_attrib, 'grab')
                if chev_good:
                    chevron, color = '🔷', 0x55acee
                    response_text = 'This is a positive chevron, it was added to your chevron inventory.'
                else:
                    chevron, color = '🔻', 0xe75a70
                    response_text = 'This is a negative chevron, it destroyed half of your other chevrons...'
                connector = 'a'
                if chev_attrib[0] in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response = discord.Embed(color=color, title=f'{chevron} You caught {connector} {chev_attrib} chevron!')
                response.description = response_text
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ I don\'t think it\'s a {chev_look} chevron.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ I don\'t know what type of chevron it is.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ I don\'t see any chevron.')
    await message.channel.send(embed=response)
