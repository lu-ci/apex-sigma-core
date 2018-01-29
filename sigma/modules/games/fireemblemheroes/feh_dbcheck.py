from .mech.feh_core import FireEmblemHeroesCore


async def feh_dbcheck(ev):
    feh_core = FireEmblemHeroesCore(ev.db)
    await feh_core.feh_dbcheck()
