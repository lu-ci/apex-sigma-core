from sigma.modules.core_functions.details.updaters.updaters import server_updater


async def server_data_join(ev, guild):
    mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
    server_updater(mem_coll, guild)
