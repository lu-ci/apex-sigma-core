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
import string

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.utilities.misc.raffle.raffleicon import get_matching_emote

raffle_loop_running = False


async def raffle_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global raffle_loop_running
    if not raffle_loop_running:
        raffle_loop_running = True
        ev.bot.loop.create_task(cycler(ev))


def extra_shuffle(some_list):
    """
    :type some_list: list[discord.Member]
    :rtype: list[discord.Member]
    """
    new_list = []
    while some_list:
        new_list.append(some_list.pop(secrets.randbelow(len(some_list))))
    return new_list


def kud_from_title(text):
    """
    :type text: str
    :rtype: int
    """
    digits = []
    for char in text:
        try:
            val = int(char)
            digits.append(val)
        except ValueError:
            pass
    return int(''.join([str(dig) for dig in digits]))


async def item_from_title(ev, text):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type text: str
    """
    item_core = await get_item_core(ev.db)
    return item_core.get_item_by_name(' '.join(text.split(' ')[2:]))


async def auto_award(ev, winner, raffle):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type winner: discord.Member
    :type raffle: dict
    """
    title = raffle.get('title', '')
    for piece in title.split('+'):
        piece = piece.strip()
        if ev.bot.cfg.pref.currency.lower() in piece.lower():
            await auto_currency(ev, winner, piece)
        else:
            await auto_item(ev, winner, piece)


async def auto_currency(ev, winner, title):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type winner: discord.Member
    :type title: str
    """
    amount = kud_from_title(title)
    await ev.db.add_resource(winner.id, 'currency', amount, ev.name, None, False)


async def auto_item(ev, winner, title):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type winner: discord.Member
    :type title: str
    """
    item = await item_from_title(ev, title)
    data_for_inv = item.generate_inventory_item()
    await ev.db.add_to_inventory(winner.id, data_for_inv)


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    raffle_coll = ev.db[ev.db.db_nam].Raffles
    while True:
        if ev.bot.is_ready():
            # noinspection PyBroadException
            try:
                now = arrow.utcnow().float_timestamp
                raffles = await raffle_coll.find({'end': {'$lt': now}, 'active': True}).to_list(None)
                if raffles:
                    for raffle in raffles:
                        cid = raffle.get('channel')
                        aid = raffle.get('author')
                        mid = raffle.get('message')
                        icon = raffle.get('icon')
                        title = raffle.get('title')
                        color = raffle.get('color')
                        channel = await ev.bot.get_channel(cid)
                        if channel:
                            await raffle_coll.update_one(raffle, {'$set': {'active': False}})
                            message = await channel.fetch_message(mid)
                            if message:
                                custom_emote = icon.startswith('<:') and icon.endswith('>')
                                if custom_emote:
                                    emote = get_matching_emote(message.guild, icon)
                                    if emote:
                                        icon = emote.name
                                contestants = []
                                reactions = message.reactions
                                for reaction in reactions:
                                    rem_nam = str(reaction.emoji)
                                    custom_rem = rem_nam.startswith('<:') and rem_nam.endswith('>')
                                    if custom_rem:
                                        rem_emote = get_matching_emote(message.guild, rem_nam)
                                        if rem_emote:
                                            rem = rem_emote.name
                                        else:
                                            rem = None
                                    else:
                                        rem = reaction.emoji
                                    if rem:
                                        if rem == icon:
                                            async for user in reaction.users():
                                                if not user.bot:
                                                    contestants.append(user)
                                            break
                                if contestants:
                                    automatic = raffle.get('automatic', False)
                                    if automatic:
                                        if not (aid in ev.bot.cfg.dsc.owners or aid == ev.bot.user.id):
                                            automatic = False
                                    contestants = extra_shuffle(contestants)
                                    draw_count = min(len(contestants), raffle.get('draw_count', 1))
                                    for _ in range(draw_count):
                                        winner = contestants.pop(secrets.randbelow(len(contestants)))
                                        amen = f'<@{aid}>'
                                        wmen = f'<@{winner.id}>'
                                        ender = '' if title[-1] in string.punctuation else '!'
                                        win_text = f'{raffle.get("icon")} Hey {amen}, {wmen} won your raffle!'
                                        win_embed = discord.Embed(color=color)
                                        win_title = f'{winner.name} won {title.lower()}{ender}'
                                        if automatic:
                                            await auto_award(ev, winner, raffle)
                                            win_embed.set_footer(text='The reward has been automatically transferred.')
                                        win_embed.set_author(name=win_title[:256], icon_url=user_avatar(winner))
                                        await channel.send(win_text, embed=win_embed)
                                        ev.log.info(f'{winner} won {aid}\'s raffle {raffle.get("id")} in {cid}.')
            except Exception as e:
                ev.log.error(e)
                pass
        await asyncio.sleep(1)
