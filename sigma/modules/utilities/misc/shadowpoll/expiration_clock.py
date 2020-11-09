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

import asyncio

import arrow
import discord

sp_xp_loop_running = False


async def expiration_clock(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global sp_xp_loop_running
    if not sp_xp_loop_running:
        sp_xp_loop_running = True
        ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    poll_coll = ev.db[ev.db.db_nam].ShadowPolls
    while True:
        if ev.bot.is_ready():
            now = arrow.utcnow().int_timestamp
            poll_files = await poll_coll.find({'settings.expires': {'$lt': now}, 'settings.active': True}).to_list(None)
            for poll_file in poll_files:
                poll_id = poll_file.get('id')
                poll_file.get('settings').update({'active': False})
                await ev.db[ev.db.db_nam].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                author = await ev.bot.get_user(poll_file.get('origin', {}).get('author'))
                if author:
                    response = discord.Embed(color=0xff3333, title=f'⏰ Your poll {poll_file["id"]} has expired.')
                    try:
                        await author.send(embed=response)
                    except discord.Forbidden:
                        pass
        await asyncio.sleep(1)
