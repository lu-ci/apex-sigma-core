from sigma.core.mechanics.statistics import StatisticsStorage

stats = None


async def ev_message(ev, message):
    global stats
    if stats is None:
        stats = StatisticsStorage(ev.db, 'message')
    stats.add_stat()
