import discord

cache = {}
complete = False


def is_done():
    return complete


def get_changed_invite(guild_id, bound_list, invites):
    invite = None
    cached = cache.get(guild_id)
    if cached is None:
        cached = []
    cache.update({guild_id: invites})
    if invites is None:
        invites = []
    if invites:
        for cached_inv in cached:
            for curr_inv in invites:
                if cached_inv.id == curr_inv.id:
                    if cached_inv.uses != curr_inv.uses:
                        if curr_inv.id in bound_list:
                            invite = curr_inv
                            break
    return invite


async def bound_role_cacher(ev):
    global complete
    for guild in ev.bot.guilds:
        if guild.me.guild_permissions.create_instant_invite:
            try:
                invites = await guild.invites()
            except discord.Forbidden:
                invites = []
            cache.update({guild.id: invites})
    complete = True
    ev.log.info('Finished caching roles.')
