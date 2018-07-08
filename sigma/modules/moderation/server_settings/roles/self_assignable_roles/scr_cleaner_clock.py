# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import asyncio

import discord

from sigma.core.mechanics.event import SigmaEvent


scr_clock_running = False


async def scr_cleaner_clock(ev: SigmaEvent):
    global scr_clock_running
    if not scr_clock_running:
        ev.bot.loop.create_task(scr_clockwork(ev))
        scr_clock_running = True


async def scr_clockwork(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            try:
                coll = ev.db[ev.db.db_nam].ServerSettings
                colored_guild_docs = await coll.find({'ColorRoles': True}).to_list(None)
                guild_ids = [gdoc.get('ServerID') for gdoc in colored_guild_docs]
                guilds = [ev.bot.get_guild(gid) for gid in guild_ids if ev.bot.get_guild(gid)]
                for guild in guilds:
                    scr_roles = [rl for rl in guild.roles if rl.name.startswith('SCR-')]
                    for scrr in scr_roles:
                        scrr_members = [scrm for scrm in scrr.members if not scrm.bot]
                        if not scrr_members:
                            try:
                                await scrr.delete()
                            except (discord.Forbidden, discord.NotFound, discord.ClientException):
                                pass
            except Exception:
                pass
            await asyncio.sleep(300)
