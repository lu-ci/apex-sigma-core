from sigma.modules.core_functions.details.updaters.updaters import member_updater


async def user_data_update(ev, before, after):
    if after and after.guild:
        mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
        await member_updater(mem_coll, after)
