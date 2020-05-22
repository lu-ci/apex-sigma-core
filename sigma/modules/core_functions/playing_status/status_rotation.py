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
import json
import os
import secrets

import aiohttp
import arrow
import discord

status_cache = []
status_loop_running = False


async def status_rotation(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global status_loop_running
    if not status_loop_running:
        await ev.bot.change_presence(activity=None, status=discord.Status.online)
        status_loop_running = True
        ev.bot.loop.create_task(status_clockwork(ev))


async def streamer_check():
    """
    :return:
    :rtype: dict or None
    """
    dat = None
    chn = os.environ['SIGMA_STREAMER']
    cid = os.environ['SIGMA_TWITCH_CLIENT']
    if chn and cid:
        url = f"https://api.twitch.tv/kraken/streams/{chn}"
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': cid
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as data:
                data = await data.read()
                dat = json.loads(data)
    return dat


async def status_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            if ev.bot.cfg.pref.status_rotation:
                if not status_cache:
                    status_files = await ev.db[ev.db.db_nam].StatusFiles.find().to_list(None)
                    [status_cache.append(status_file.get('text')) for status_file in status_files]
                if status_cache:
                    stream = await streamer_check()
                    if stream:
                        stream = stream.get('stream', {})
                        channel = stream.get('channel', {})
                        activity = discord.Streaming(
                            name=channel.get('status'),
                            url=channel.get('url'),
                            game=stream.get('game')
                        )
                    else:
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
