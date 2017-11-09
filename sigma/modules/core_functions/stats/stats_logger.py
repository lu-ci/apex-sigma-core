import asyncio

import arrow


async def stats_logger(ev):
    ev.bot.loop.create_task(population_insert_clock(ev))


async def population_insert_clock(ev):
    while True:
        if not ev.bot.cool_down.on_cooldown(ev.name, 'stats_logger'):
            ev.bot.cool_down.set_cooldown(ev.name, 'stats_logger', 3600)
            collection = 'StatisticsLogs'
            database = ev.bot.cfg.db.database
            server_count = len(list(ev.bot.guilds))
            member_count = len(list(ev.bot.get_all_members()))
            channel_count = len(list(ev.bot.get_all_channels()))
            command_count = ev.db[database].CommandStats.count()
            stat_data = {
                'stamp': arrow.utcnow().timestamp,
                'guilds': server_count,
                'users': member_count,
                'channels': channel_count,
                'commands': command_count
            }
            ev.db[database][collection].insert_one(stat_data)
        await asyncio.sleep(300)
