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

import asyncio

import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar

rem_loop_running = False


async def reminder_clockwork(ev: SigmaEvent):
    global rem_loop_running
    if not rem_loop_running:
        rem_loop_running = True
        ev.bot.loop.create_task(reminder_cycler(ev))


async def reminder_cycler(ev: SigmaEvent):
    coll = ev.db[ev.db.db_nam].Reminders
    while True:
        if ev.bot.is_ready():
            current_stamp = arrow.utcnow().timestamp
            reminders = await coll.find({'execution_stamp': {'$lt': current_stamp}}).to_list(None)
            if reminders:
                for reminder in reminders:
                    is_dm = reminder.get('direct_message')
                    channel = await ev.bot.get_channel(reminder.get('channel_id'))
                    author = await ev.bot.get_user(reminder.get('user_id'))
                    if channel and not is_dm:
                        target = channel
                    elif author or is_dm:
                        target = author
                    else:
                        target = None
                    if target:
                        await coll.delete_one(reminder)
                        dt_stamp = arrow.get(reminder.get('creation_stamp')).datetime
                        title = '⏰ Your Reminder'
                        response = discord.Embed(color=0xff3333, title=title, timestamp=dt_stamp)
                        response.description = reminder.get('text_message')
                        if author:
                            response.set_author(name=author.name, icon_url=user_avatar(author))
                        response.set_footer(text=f'Reminder: {reminder.get("reminder_id")}')
                        try:
                            if author:
                                await target.send(f'{author.mention}, your reminder executed.', embed=response)
                            else:
                                await target.send(embed=response)
                        except discord.ClientException:
                            pass
        await asyncio.sleep(1)
