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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


async def reminderinfo(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        rem_id = pld.args[0].lower()
        lookup_data = {'user_id': pld.msg.author.id, 'reminder_id': rem_id}
        reminder = await cmd.db.col.Reminders.find_one(lookup_data)
        if reminder:
            execution_stamp = reminder['execution_stamp']
            text_message = reminder['text_message']
            timestamp = arrow.get(execution_stamp).datetime
            human_time = arrow.get(execution_stamp).humanize(arrow.utcnow())
            auth_title = f'{pld.msg.author.display_name}\'s Reminder: {rem_id}'
            channel = await cmd.bot.get_channel(reminder.get('channel_id'))
            if channel:
                chan_name = f'**#{channel.name}**'
                srv_name = f'**{channel.guild.name}**'
            else:
                chan_name = '*{No Channel}*'
                srv_name = '*{No Server}*'
            location_text = f'Executes in {chan_name} on {srv_name} {human_time}.'
            response = discord.Embed(color=0x66CC66, timestamp=timestamp)
            response.add_field(name='🏛 Location', value=location_text, inline=False)
            response.add_field(name='🗒 Reminder Text', value=text_message, inline=False)
            response.set_author(name=auth_title, icon_url=user_avatar(pld.msg.author))
        else:
            response = GenericResponse(f'Reminder `{rem_id}` not found.').not_found()
    else:
        response = GenericResponse('Missing reminder ID.').error()
    await pld.msg.channel.send(embed=response)
