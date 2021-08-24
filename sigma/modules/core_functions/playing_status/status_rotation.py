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
import secrets

import discord

from sigma.modules.searches.twitch.partner_monitor import is_live

status_cache = []
status_loop_running = False


async def status_rotation(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global status_loop_running
    if not status_loop_running:
        # noinspection PyBroadException
        try:
            await ev.bot.change_presence(activity=None, status=discord.Status.online)
        except Exception:
            ev.log.warn('Initial presence clearing failed.')
        status_loop_running = True
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            if ev.bot.cfg.pref.status_rotation and not is_live():
                if not status_cache:
                    status_files = await ev.db[ev.db.db_nam].StatusFiles.find().to_list(None)
                    [status_cache.append(status_file.get('text')) for status_file in status_files]
                if status_cache:
                    status = status_cache.pop(secrets.randbelow(len(status_cache)))
                    activity = discord.Activity(name=status, type=discord.ActivityType.playing)
                    # noinspection PyBroadException
                    try:
                        if ev.bot.cfg.pref.dev_mode:
                            status_type = discord.Status.dnd
                        else:
                            if ev.bot.latency > 5 or ev.bot.latency < 0:
                                status_type = discord.Status.dnd
                            elif ev.bot.latency > 2:
                                status_type = discord.Status.idle
                            else:
                                status_type = discord.Status.online
                        await ev.bot.change_presence(activity=activity, status=status_type)
                    except Exception:
                        pass
        await asyncio.sleep(60)
