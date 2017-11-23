from sigma.modules.core_functions.details.updaters.updaters import member_updater


async def user_data_join(ev, member):
    if member and member.guild:
        mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
        member_updater(mem_coll, member)
