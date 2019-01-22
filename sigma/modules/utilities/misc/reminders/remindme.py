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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import convert_to_seconds, user_avatar
from sigma.core.utilities.generic_responses import error


async def remindme(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        time_req = pld.args[0]
        try:
            in_seconds = convert_to_seconds(time_req)
            upper_limit = 7776000
            if in_seconds <= upper_limit:
                rem_count = await cmd.db[cmd.db.db_nam].Reminders.count_documents({'user_id': pld.msg.author.id})
                rem_limit = 15
                if rem_count < rem_limit:
                    is_dm = False
                    if len(pld.args) > 1:
                        if pld.args[-1].lower() == '--direct':
                            is_dm = True
                            text_message = ' '.join(pld.args[1:-1])
                            text_message = 'No reminder message set.' if not text_message else text_message
                        else:
                            text_message = ' '.join(pld.args[1:])
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
                        'reminder_id':     reminder_id,
                        'user_id':         pld.msg.author.id,
                        'creation_stamp':  arrow.utcnow().timestamp,
                        'execution_stamp': execution_stamp,
                        'channel_id':      pld.msg.channel.id,
                        'server_id':       pld.msg.guild.id,
                        'text_message':    text_message,
                        'direct_message':  is_dm
                    }
                    await cmd.db[cmd.db.db_nam].Reminders.insert_one(reminder_data)
                    response = discord.Embed(color=0x66CC66, timestamp=timestamp)
                    response.description = text_message
                    response.set_author(name=f'Reminder {reminder_id} Created', icon_url=user_avatar(pld.msg.author))
                    response.set_footer(text=f'Executes: {time_diff.title()}')
                else:
                    response = error('You already have 15 reminders pending.')
            else:
                response = error('Reminders have a limit of 90 days.')
        except (LookupError, ValueError):
            response = error('Please use the format HH:MM:SS.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
