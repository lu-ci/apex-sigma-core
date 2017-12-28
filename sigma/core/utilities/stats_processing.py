from sigma.modules.core_functions.stats.stats_temp_storage import StatisticsStorage

stats_handler = None


async def add_cmd_stat(cmd):
    lookup_target = {'command': cmd.name}
    stat_file = await cmd.db[cmd.db.db_cfg.database]['CommandStats'].find_one(lookup_target)
    if stat_file:
        count = stat_file.get('count')
        await cmd.db[cmd.db.db_cfg.database]['CommandStats'].update_one(lookup_target, {'$set': {'count': count}})
    else:
        count = 1
        await cmd.db[cmd.db.db_cfg.database]['CommandStats'].insert_one({'name': cmd.name, 'count': count})


async def add_special_stats(db, stat_name):
    global stats_handler
    if not stats_handler:
        stats_handler = StatisticsStorage(db, stat_name)
    stats_handler.add_stat()
