from sigma.modules.core_functions.details.updaters.updaters import server_updater


async def server_data_update(ev, before, after):
    if before.name != after.name or before.icon != after.icon:
        mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
        await server_updater(mem_coll, after)
