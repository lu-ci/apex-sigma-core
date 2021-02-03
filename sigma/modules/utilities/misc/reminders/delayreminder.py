"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import arrow
import discord

from sigma.core.utilities.data_processing import convert_to_seconds
from sigma.core.utilities.generic_responses import GenericResponse


async def delayreminder(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) == 2:
            rem_id = pld.args[0].lower()
            lookup_data = {'user_id': pld.msg.author.id, 'reminder_id': rem_id}
            reminder = await cmd.db[cmd.db.db_nam].Reminders.find_one(lookup_data)
            if reminder:
                try:
                    time_req = pld.args[1]
                    upper_limit = 7776000
                    in_seconds = convert_to_seconds(time_req)
                    execution_stamp = reminder.get('execution_stamp') + in_seconds
                    expires_in = execution_stamp - arrow.utcnow().int_timestamp
                    if expires_in <= upper_limit:
                        timestamp = arrow.get(execution_stamp).datetime
                        if execution_stamp < 60:
                            time_diff = f'In {in_seconds} seconds'
                        else:
                            time_diff = arrow.get(execution_stamp + 5).humanize(arrow.utcnow())
                        reminder.update({'execution_stamp': execution_stamp})
                        await cmd.db[cmd.db.db_nam].Reminders.update_one(lookup_data, {'$set': reminder})
                        response = discord.Embed(color=0x66CC66, timestamp=timestamp)
                        response.title = f'✅ Reminder {rem_id} has been delayed.'
                        response.set_footer(text=f'Executes: {time_diff.title()}')
                    else:
                        response = GenericResponse('Reminders have a limit of 90 days.').error()
                except (LookupError, ValueError):
                    response = GenericResponse('Please use the format HH:MM:SS.').error()
            else:
                response = GenericResponse(f'Reminder `{rem_id}` not found.').not_found()
        else:
            response = GenericResponse('Invalid number of arguments.').error()
    else:
        response = GenericResponse('Missing reminder ID and duration.').error()
    await pld.msg.channel.send(embed=response)
