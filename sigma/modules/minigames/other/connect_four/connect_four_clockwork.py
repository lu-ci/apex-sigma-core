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

from sigma.modules.minigames.other.connect_four.connect_four_mechanics import cf_cache
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

cf_loop_running = False


async def connect_four_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global cf_loop_running
    if not cf_loop_running:
        cf_loop_running = True
        ev.bot.loop.create_task(connect_four_cycler(ev))


async def connect_four_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            # noinspection PyBroadException
            try:
                games = cf_cache.cache.items()
                for mid, game in games:
                    expiry = game.expiry
                    now = arrow.utcnow().int_timestamp
                    if now > expiry:
                        channel = await ev.bot.get_channel(game.channel_id)
                        if channel:
                            wait_cycles = 0
                            while Ongoing.is_ongoing('cf_ongoing_turn', channel.id) and wait_cycles < 5:
                                wait_cycles += 1
                                await asyncio.sleep(1)
                            timeout_title = '🕙 Time\'s up'
                            try:
                                timeout_title += ' ' + game.current_turn.display_name + '!'
                            except AttributeError:
                                timeout_title += '!'
                            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                            try:
                                await channel.send(embed=timeout_embed)
                            except (discord.NotFound, discord.Forbidden):
                                pass
                            if Ongoing.is_ongoing('connectfour', channel.id):
                                Ongoing.del_ongoing('connectfour', channel.id)
                            if Ongoing.is_ongoing('cf_ongoing_turn', channel.id):
                                Ongoing.del_ongoing('cf_ongoing_turn', channel.id)
                            await cf_cache.del_cache(mid)
            except Exception:
                pass
        await asyncio.sleep(5)
