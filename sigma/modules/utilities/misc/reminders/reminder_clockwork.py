# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import asyncio

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


async def reminder_clockwork(ev):
    ev.bot.loop.create_task(clockwork_function_reminder_clockwork(ev))


async def clockwork_function_reminder_clockwork(ev):
    while ev.bot.is_ready():
        reminders = await ev.db[ev.db.db_cfg.database]['Reminders'].find({}).to_list(None)
        for reminder in reminders:
            current_stamp = arrow.utcnow().timestamp
            execution_stamp = reminder['ExecutionStamp']
            if current_stamp > execution_stamp:
                await ev.db[ev.db.db_cfg.database]['Reminders'].delete_one({'ReminderID': reminder['ReminderID']})
                channel = discord.utils.find(lambda x: x.id == reminder['ChannelID'], ev.bot.get_all_channels())
                author = discord.utils.find(lambda x: x.id == reminder['UserID'], ev.bot.get_all_members())
                if channel:
                    target = channel
                elif author:
                    target = author
                else:
                    target = None
                if target:
                    dt_stamp = arrow.get(reminder['CreationStamp']).datetime
                    title = f'⏰ Your Reminder'
                    response = discord.Embed(color=0xff3333, title=title, timestamp=dt_stamp)
                    response.description = reminder.get('TextMessage')
                    if author:
                        response.set_author(name=author.name, icon_url=user_avatar(author))
                    response.set_footer(text=f'Reminder: {reminder.get("ReminderID")}')
                    try:
                        if author:
                            await target.send(f'{author.mention}, your reminder executed.', embed=response)
                        else:
                            await target.send(embed=response)
                    except discord.ClientException:
                        pass
        await asyncio.sleep(1)
