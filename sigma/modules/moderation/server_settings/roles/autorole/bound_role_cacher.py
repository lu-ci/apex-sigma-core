# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
import asyncio

cache = {}
changes = {}


def update_invites(guild, invites):
    cache.update({guild.id: invites})


def get_changed_invite(guild_id, member_id, bound_list, invites):
    invite = changes.get(f'{guild_id}_{member_id}')
    cached = cache.get(guild_id)
    cache.update({guild_id: invites})
    if cached is None:
        cached = []
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
    counter = 0
    ev.log.info('Starting invite caching...')
    for guild in ev.bot.guilds:
        has_bound_invs = await ev.db.get_guild_settings(guild.id, 'BoundInvites')
        has_bound_greets = await ev.db.get_guild_settings(guild.id, 'BoundGreetings')
        if has_bound_invs or has_bound_greets:
            if guild.me.guild_permissions.create_instant_invite:
                try:
                    invites = await guild.invites()
                    counter += 1
                except discord.Forbidden:
                    invites = []
                cache.update({guild.id: invites})
    ev.log.info(f'Finished caching invites for {counter} guilds.')
    ev.bot.loop.create_task(change_cleaner())


async def change_cleaner():
    global changes
    while True:
        changes = {}
        await asyncio.sleep(300)
