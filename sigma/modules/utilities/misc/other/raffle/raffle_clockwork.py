import asyncio
import secrets
import string

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


async def raffle_clockwork(ev):
    ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    raffle_coll = ev.db[ev.db.db_cfg.database].Raffles
    while ev.bot.is_ready():
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
                        win_embed.set_author(name=f'{winner.name} won {titl.lower()}{ender}', icon_url=user_avatar(winner))
                        await channel.send(win_text, embed=win_embed)
        await asyncio.sleep(1)
