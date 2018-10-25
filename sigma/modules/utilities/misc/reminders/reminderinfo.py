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


async def reminderinfo(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        rem_id = args[0].lower()
        lookup_data = {'user_id': message.author.id, 'reminder_id': rem_id}
        reminder = await cmd.db[cmd.db.db_nam].Reminders.find_one(lookup_data)
        if reminder:
            execution_stamp = reminder['execution_stamp']
            text_message = reminder['text_message']
            timestamp = arrow.get(execution_stamp).datetime
            human_time = arrow.get(execution_stamp).humanize(arrow.utcnow())
            auth_title = f'{message.author.display_name}\'s Reminder: {rem_id}'
            channel = cmd.bot.get_channel(reminder.get('channel_id'))
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
            response.set_author(name=auth_title, icon_url=user_avatar(message.author))
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Reminder `{rem_id}` not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing reminder ID.')
    await message.channel.send(embed=response)
