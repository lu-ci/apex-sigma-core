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
from sigma.core.utilities.data_processing import user_avatar


async def shadowpollview(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        poll_id = ''.join(args).lower()
        poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            active = poll_file.get('settings', {}).get('active')
            visible = poll_file.get('settings', {}).get('visible')
            author_id = poll_file.get('origin', {}).get('author')
            if active or visible or author_id == message.author.id:
                response = discord.Embed(color=0xF9F9F9, title=poll_file.get('poll', {}).get('question'))
                author = cmd.bot.get_user(author_id)
                if author:
                    response.set_author(name=author.name, icon_url=user_avatar(author))
                else:
                    response.set_author(name=f'{author_id}', icon_url='https://i.imgur.com/QnYSlld.png')
                expiration = poll_file.get('settings', {}).get('expires')
                if expiration is not None:
                    exp_dt = arrow.get(expiration).datetime
                    exp_hum = arrow.get(expiration).humanize()
                    response.set_footer(text=f'Expires {exp_hum}')
                    response.timestamp = exp_dt
                else:
                    created = poll_file.get('created')
                    cre_dt = arrow.get(created).datetime
                    cre_hum = arrow.get(created).humanize()
                    response.set_footer(text=f'Created {cre_hum}')
                    response.timestamp = cre_dt
                loop_index = 0
                answer_lines = []
                for answer in poll_file.get('poll', {}).get('answers'):
                    loop_index += 1
                    answer_line = f'**{loop_index}**: {answer}'
                    answer_lines.append(answer_line)
                answers = '\n'.join(answer_lines)
                response.description = answers
            else:
                response = discord.Embed(color=0xFFCC4D, title='🔒 That poll is not active.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 Poll not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
