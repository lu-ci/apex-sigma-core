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

import secrets

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar, convert_to_seconds


async def remindme(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        time_req = args[0]
        try:
            in_seconds = convert_to_seconds(time_req)
            upper_limit = 7776000
            if in_seconds <= upper_limit:
                rem_count = await cmd.db[cmd.db.db_nam].Reminders.count_documents({'user_id': message.author.id})
                rem_limit = 15
                if rem_count < rem_limit:
                    if len(args) > 1:
                        text_message = ' '.join(args[1:])
                    else:
                        text_message = 'No reminder message set.'
                    execution_stamp = arrow.utcnow().timestamp + in_seconds
                    timestamp = arrow.get(execution_stamp).datetime
                    if in_seconds < 60:
                        time_diff = f'In {in_seconds} seconds'
                    else:
                        time_diff = arrow.get(execution_stamp + 5).humanize(arrow.utcnow())
                    reminder_id = secrets.token_hex(2)
                    reminder_data = {
                        'reminder_id': reminder_id,
                        'user_id': message.author.id,
                        'creation_stamp': arrow.utcnow().timestamp,
                        'execution_stamp': execution_stamp,
                        'channel_id': message.channel.id,
                        'server_id': message.guild.id,
                        'text_message': text_message
                    }
                    await cmd.db[cmd.db.db_nam].Reminders.insert_one(reminder_data)
                    response = discord.Embed(color=0x66CC66, timestamp=timestamp)
                    response.description = text_message
                    response.set_author(name=f'Reminder {reminder_id} Created', icon_url=user_avatar(message.author))
                    response.set_footer(text=f'Executes: {time_diff.title()}')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You already have 15 reminders pending.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Reminders have a limit of 90 days.')
        except (LookupError, ValueError):
            response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
