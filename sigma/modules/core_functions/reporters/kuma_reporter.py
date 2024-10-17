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
import os

import aiohttp

kuma_loop_running = False


async def kuma_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global kuma_loop_running
    if not kuma_loop_running:
        kuma_endpoint = os.environ.get('KUMA_ENDPOINT')
        if kuma_endpoint:
            kuma_loop_running = True
            ev.bot.loop.create_task(kuma_reporter_cycler(ev))


async def kuma_reporter_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        ready = ev.bot.is_ready()
        status = 'up' if ready else 'down'
        message = 'ACTIVE' if ready else 'INACTIVE'
        kuma_endpoint = os.environ.get('KUMA_ENDPOINT')
        uri = f'{kuma_endpoint}?status={status}&msg={message}'
        if ready:
            try:
                latency = int(ev.bot.latency * 1000)
            except OverflowError:
                latency = 999
            uri += f'&ping={latency}'
        # noinspection PyBroadException
        try:
            async with aiohttp.ClientSession() as session:
                await session.get(uri)
        except Exception:
            pass
        await asyncio.sleep(30)
