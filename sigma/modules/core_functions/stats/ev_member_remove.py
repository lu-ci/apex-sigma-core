from .stats_temp_storage import StatisticsStorage

stats = None


async def ev_member_remove(ev, message):
    global stats
    if stats is None:
        stats = StatisticsStorage(ev.db, 'member_remove')
    stats.add_stat()
