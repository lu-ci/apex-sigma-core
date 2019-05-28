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

from sigma.modules.owner_controls.leaderboards.awardleaderboards import reset_resource

leaderboard_loop_running = False


async def leaderboard_clock(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global leaderboard_loop_running
    if not leaderboard_loop_running:
        leaderboard_loop_running = True
        ev.bot.loop.create_task(leaderboard_clockwork(ev))


async def leaderboard_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    if 0 in (ev.bot.shard_ids or [0]):
        while True:
            if ev.bot.is_ready():
                first = arrow.utcnow().format('D') == '1'
                if first:
                    lookup = {'date': arrow.utcnow().format('YYYY-MM-DD')}
                    exists = await ev.db[ev.db.db_nam].LeaderboardClockworkCache.find_one(lookup)
                    if not exists:
                        ev.log.info('Resetting monthly leaderboards...')
                        await ev.db[ev.db.db_nam].LeaderboardClockworkCache.insert_one(lookup)
                        for res in ['Cookies', 'Currency']:
                            await reset_resource(ev.db, ev.log, res)
                        ev.log.info('Finished resetting monthly leaderboards.')
            await asyncio.sleep(60)
