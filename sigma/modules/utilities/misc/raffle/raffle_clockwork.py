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

    :param some_list:
    :type some_list:
    :return:
    :rtype:
    """
    new_list = []
    while some_list:
        new_list.append(some_list.pop(secrets.randbelow(len(some_list))))
    return new_list


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
                        titl = raffle.get('title')
                        colr = raffle.get('color')
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
                                    contestants = extra_shuffle(contestants)
                                    winner = secrets.choice(contestants)
                                    amen = f'<@{aid}>'
                                    wmen = f'<@{winner.id}>'
                                    ender = '' if titl[-1] in string.punctuation else '!'
                                    win_text = f'{raffle.get("icon")} Hey {amen}, {wmen} won your raffle!'
                                    win_embed = discord.Embed(color=colr)
                                    win_title = f'{winner.name} won {titl.lower()}{ender}'
                                    win_embed.set_author(name=win_title, icon_url=user_avatar(winner))
                                    await channel.send(win_text, embed=win_embed)
                                    ev.log.info(f'{winner} won {aid}\'s raffle {raffle.get("ID")} in {cid}.')
            except Exception as e:
                ev.log.error(e)
                pass
        await asyncio.sleep(1)
