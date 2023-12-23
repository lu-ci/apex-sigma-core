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

scr_clock_running = False


async def scr_cleaner_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global scr_clock_running
    if not scr_clock_running:
        ev.bot.loop.create_task(scr_cleaner_cycler(ev))
        scr_clock_running = True


async def scr_cleaner_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            # noinspection PyBroadException
            try:
                colored_guild_docs = await ev.db.col.ServerSettings.find({'color_roles': True}).to_list(None)
                guild_ids = [gdoc.get('server_id') for gdoc in colored_guild_docs]
                guilds = [await ev.bot.get_guild(gid) for gid in guild_ids if await ev.bot.get_guild(gid)]
                for guild in guilds:
                    scr_roles = [rl for rl in guild.roles if rl.name.startswith('SCR-')]
                    for scrr in scr_roles:
                        scrr_members = [scrm for scrm in scrr.members if not scrm.bot]
                        if not scrr_members:
                            try:
                                await scrr.delete()
                                ev.log.info(f'Deleted {scrr.name} [{scrr.id}] on {guild.name} [{guild.id}]')
                            except (discord.Forbidden, discord.NotFound, discord.ClientException):
                                pass
                            await asyncio.sleep(5)
            except Exception:
                pass
            await asyncio.sleep(300)
