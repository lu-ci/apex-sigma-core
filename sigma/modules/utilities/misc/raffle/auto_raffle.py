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
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
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


def thousand_separator(number):
    out = []
    for (ix, dig) in enumerate(reversed(str(number))):
        out.append(dig)
        if (ix + 1) % 3 == 0:
            out.append(',')
    return ''.join(reversed(out))


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    cfg = ev.bot.modules.commands.get('raffle').cfg
    cfg_args = ['winners', 'reward', 'interval', 'duration', 'item_chance', 'mixed_chance']
    if all([bool(getattr(cfg, arg)) for arg in cfg_args]):
        while True:
            ch = await ev.bot.get_channel(cfg.channel)
            if ch:
                lookup = {'automatic': True, 'author': ev.bot.user.id}
                auto_docs = await ev.db[ev.db.db_nam].Raffles.find(lookup).sort('start', -1).to_list(None)
                if auto_docs:
                    latest = auto_docs[0]
                    now = arrow.utcnow().float_timestamp
                    stamp = latest.get('start', 0)
                    if now > stamp + cfg.interval:
                        await create(ev, ch)
                else:
                    await create(ev, ch)
            await asyncio.sleep(60)


async def create(ev, ch):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type ch: discord.TextChannel
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
    resp_title = f"Auto-Raffle {rafid} has begun!"
    reaction_name = reaction_icon = secrets.choice(raffle_icons)
    icon_color = icon_colors.get(reaction_icon)
    roll = secrets.randbelow(100)
    if roll < cfg.mixed_chance:
        raffle_title = f"{thousand_separator(int(cfg.reward * 0.85))} {ev.bot.cfg.pref.currency}"
        item_core = await get_item_core(ev.db)
        item = item_core.pick_item_in_rarity(secrets.choice(['fish', 'plant', 'animal']), secrets.randbelow(4) + 5)
        connector = 'an' if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u'] else 'a'
        raffle_title += f" + {connector.title()} {item.rarity_name.title()} {item.name}"
    elif roll < cfg.item_chance:
        item_core = await get_item_core(ev.db)
        item = item_core.pick_item_in_rarity(secrets.choice(['fish', 'plant', 'animal']), secrets.randbelow(4) + 5)
        connector = 'an' if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u'] else 'a'
        raffle_title = f"{connector.title()} {item.rarity_name.title()} {item.name}"
    else:
        raffle_title = f"{thousand_separator(cfg.reward)} {ev.bot.cfg.pref.currency}"
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
