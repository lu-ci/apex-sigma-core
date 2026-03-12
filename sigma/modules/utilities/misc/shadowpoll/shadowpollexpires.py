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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.misc.reminders.remindme import convert_to_seconds


async def shadowpollexpires(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) == 2:
            poll_id = pld.args[0].lower()
            time_input = pld.args[1]
            try:
                exp_in = convert_to_seconds(time_input)
                poll_file = await cmd.db.col.ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    if poll_file['origin']['author'] == pld.msg.author.id:
                        end_stamp = arrow.utcnow().float_timestamp + exp_in
                        end_human = arrow.get(end_stamp).humanize()
                        end_datet = arrow.get(end_stamp).datetime
                        poll_file['settings'].update({'expires': end_stamp})
                        await cmd.db.col.ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                        title = f'⏰ Poll set to expire {end_human}.'
                        response = discord.Embed(color=0xff3333, title=title, timestamp=end_datet)
                    else:
                        response = GenericResponse('You didn\'t make this poll.').denied()
                else:
                    response = GenericResponse('Poll not found.').not_found()
            except (LookupError, ValueError):
                response = GenericResponse('Please use the format HH:MM:SS.').error()
        else:
            response = GenericResponse('Missing arguments.').error()
    else:
        response = GenericResponse('Missing poll ID and expiration time.').error()
    await pld.msg.channel.send(embed=response)
