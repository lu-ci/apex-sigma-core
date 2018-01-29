import asyncio

import arrow
import discord


async def expiration_clock(ev):
    ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    poll_coll = ev.db[ev.db.db_cfg.database].ShadowPolls
    while ev.bot.is_ready():
        now = arrow.utcnow().timestamp
        poll_files = await poll_coll.find({'settings.expires': {'$lt': now}, 'settings.active': True}).to_list(None)
        for poll_file in poll_files:
            poll_id = poll_file['id']
            poll_file['settings'].update({'active': False})
            await ev.db[ev.db.db_cfg.database].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
            author = discord.utils.find(lambda x: x.id == poll_file['origin']['author'], ev.bot.get_all_members())
            if author:
                response = discord.Embed(color=0xff3333, title=f'⏰ Your poll {poll_file["id"]} has expired.')
                try:
                    await author.send(embed=response)
                except discord.Forbidden:
                    pass
        await asyncio.sleep(1)
