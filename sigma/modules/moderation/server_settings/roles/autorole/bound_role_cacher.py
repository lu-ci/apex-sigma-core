"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio

import discord

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig

invite_cache = MemoryCacher(CacheConfig({}))


async def update_invites(guild, invites):
    """
    :type guild: discord.Guild
    :type invites: list
    """
    cache_key = f'invite_cache_{guild.id}'
    cache = await invite_cache.get_cache(cache_key) or {}
    cache.update({guild.id: invites})
    await invite_cache.set_cache(cache_key, cache)


async def get_changed_invite(guild_id, bound_list, invites):
    """
    Checks for invite count changes to get the one that triggered.
    :type guild_id: int
    :type bound_list: list
    :type invites: list
    :rtype: discord.Invite
    """
    invite = None
    cache_key = f'invite_cache_{guild_id}'
    cache = await invite_cache.get_cache(cache_key) or {}
    cached = cache.get(guild_id)
    if cached is None:
        cached = []
    cache.update({guild_id: invites})
    await invite_cache.set_cache(cache_key, cache)
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


async def update_cache(guild):
    """
    Updates the cache with fresh invites.
    :type guild: discord.Guild
    """
    try:
        invites = await guild.invites()
    except discord.Forbidden:
        invites = []
    await update_invites(guild, invites)


async def bound_role_cacher(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    ev.log.info('Starting invite caching...')
    counter = 0
    for guild in ev.bot.guilds:
        if await ev.db.get_guild_settings(guild.id, 'bound_invites'):
            if guild.me.guild_permissions.create_instant_invite:
                counter += 1
                await update_cache(guild)
                await asyncio.sleep(5)
    ev.log.info(f'Finished caching invites for {counter} guilds.')
