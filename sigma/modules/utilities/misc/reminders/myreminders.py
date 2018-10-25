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
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.data_processing import user_avatar


async def myreminders(cmd: SigmaCommand, pld: CommandPayload):
    here = False
    if args:
        if args[-1].lower() == 'here':
            here = True
    if here:
        lookup_data = {'user_id': message.author.id, 'channel_id': message.channel.id}
    else:
        lookup_data = {'user_id': message.author.id}
    all_reminders = cmd.db[cmd.db.db_nam].Reminders
    reminder_count = await all_reminders.count_documents(lookup_data)
    all_reminders = await all_reminders.find(lookup_data).to_list(None)
    if reminder_count:
        ender = 'reminder' if reminder_count == 1 else 'reminders'
        if here:
            reminder_list_title = f'You have {reminder_count} pending {ender} in #{message.channel.name}.'
        else:
            reminder_list_title = f'You have {reminder_count} pending {ender}.'
        reminder_list = ''
        for reminder in all_reminders:
            human_time = arrow.get(reminder.get('execution_stamp')).humanize(arrow.utcnow())
            channel = cmd.bot.get_channel(reminder.get('channel_id'))
            if channel:
                chan_name = f'**#{channel.name}**'
                srv_name = f'**{channel.guild.name}**'
            else:
                chan_name = '*{No Channel}*'
                srv_name = '*{No Server}*'
            rem_id = reminder['reminder_id']
            reminder_list += f'\n`{rem_id}` in {chan_name} on {srv_name} {human_time}'
        strip_clr = await get_image_colors(user_avatar(message.author))
        response = discord.Embed(color=strip_clr)
        response.set_author(name=f'{message.author.display_name}\'s Reminders', icon_url=user_avatar(message.author))
        response.add_field(name='Reminder Count', value=reminder_list_title, inline=False)
        response.add_field(name='Reminder List', value=reminder_list, inline=False)
    else:
        response = discord.Embed(color=0x696969, title='🔍 You have no pending reminders.')
    await message.channel.send(embed=response)
