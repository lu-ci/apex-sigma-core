# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import secrets
import string

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


raffle_loop_running = False


async def raffle_clockwork(ev):
    global raffle_loop_running
    if not raffle_loop_running:
        raffle_loop_running = True
        ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    raffle_coll = ev.db[ev.db.db_cfg.database].Raffles
    while True:
        if ev.bot.is_ready():
            now = arrow.utcnow().float_timestamp
            raffle = await raffle_coll.find_one({'End': {'$lt': now}, 'Active': True})
            if raffle:
                await raffle_coll.update_one(raffle, {'$set': {'Active': False}})
                cid = raffle.get('Channel')
                aid = raffle.get('Author')
                mid = raffle.get('Message')
                icon = raffle.get('Icon')
                titl = raffle.get('Title')
                colr = raffle.get('Color')
                channel = discord.utils.find(lambda x: x.id == cid, ev.bot.get_all_channels())
                if channel:
                    message = await channel.get_message(mid)
                    if message:
                        contestants = []
                        reactions = message.reactions
                        for reaction in reactions:
                            if reaction.emoji == icon:
                                async for user in reaction.users():
                                    if not user.bot:
                                        contestants.append(user)
                                break
                        if contestants:
                            winner = secrets.choice(contestants)
                            amen = f'<@{aid}>'
                            wmen = f'<@{winner.id}>'
                            ender = '' if titl[-1] in string.punctuation else '!'
                            win_text = f'{icon} Hey {amen}, {wmen} won your raffle!'
                            win_embed = discord.Embed(color=colr)
                            win_embed.set_author(name=f'{winner.name} won {titl.lower()}{ender}',
                                                 icon_url=user_avatar(winner))
                            await channel.send(win_text, embed=win_embed)
        await asyncio.sleep(1)
