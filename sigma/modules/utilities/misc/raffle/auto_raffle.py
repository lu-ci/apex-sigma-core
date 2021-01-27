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

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.utilities.misc.raffle.raffle import raffle_icons, icon_colors

auto_raffle_loop_running = False


async def auto_raffle(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global auto_raffle_loop_running
    if not auto_raffle_loop_running:
        auto_raffle_loop_running = True
        ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    cfg = ev.bot.modules.commands.get('raffle').cfg
    if cfg.channel:
        if cfg.winners:
            if cfg.reward:
                if cfg.interval:
                    if cfg.duration:
                        ev.log.info('cfg ok')
                        while True:
                            ev.log.info(cfg.channel)
                            ch = await ev.bot.get_channel(cfg.channel)
                            ev.log.info(ch)
                            if ch:
                                ev.log.info('ch ok')
                                auto_docs = await ev.db[ev.db.db_nam].Raffles.find({'automatic': True}).sort('start',
                                                                                                             -1).to_list(
                                    None)
                                if auto_docs:
                                    ev.log.info('yes docs')
                                    latest = auto_docs[0]
                                    now = arrow.utcnow().float_timestamp
                                    stamp = latest.get('start_stamp', 0)
                                    if now > stamp + cfg.interval:
                                        await create(ev, ch, len(auto_docs))
                                else:
                                    ev.log.info('no docs')
                                    await create(ev, ch, len(auto_docs))
                            await asyncio.sleep(60)


async def create(ev, ch, count):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param ch: The auto-raffle channel.
    :type ch: discord.TextChannel
    :param count: Number of existing documents.
    :type count: int
    """
    cfg = ev.bot.modules.commands.get('raffle').cfg
    draw_count = cfg.winners
    start_stamp = arrow.utcnow().float_timestamp
    end_stamp = start_stamp + cfg.duration
    if cfg.duration < 90:
        end_hum = f"in {cfg.duration} seconds"
    else:
        end_hum = arrow.get(end_stamp).humanize()
    end_dt = arrow.get(end_stamp).datetime
    rafid = secrets.token_hex(3)
    resp_title = f"Auto-Raffle #{count + 1} has begun!"
    reaction_name = reaction_icon = secrets.choice(raffle_icons)
    icon_color = icon_colors.get(reaction_icon)
    raffle_title = f"{cfg.reward} {ev.bot.cfg.pref.currency}"
    starter = discord.Embed(color=icon_color, timestamp=end_dt)
    starter.set_author(name=resp_title, icon_url=(user_avatar(ev.bot.user)))
    starter.description = f"Prize: **{raffle_title}**"
    if draw_count > 1:
        starter.description += f"\nWinners: **{draw_count}**"
    starter.description += f"\nReact with a {reaction_icon} to enter the raffle."
    starter.set_footer(text=f"[{rafid}] Raffle ends {end_hum}.")
    starter_message = await ch.send(embed=starter)
    await starter_message.add_reaction(reaction_icon)
    raffle_data = {
        'automatic': True,
        'author': ev.bot.user.id,
        'channel': cfg.channel,
        'title': raffle_title,
        'start': start_stamp,
        'end': end_stamp,
        'icon': reaction_name,
        'color': icon_color,
        'draw_count': draw_count,
        'message': starter_message.id,
        'active': True,
        'id': rafid
    }
    await ev.db[ev.db.db_nam].Raffles.insert_one(raffle_data)
