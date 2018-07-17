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

import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent


unpun_loop_running = False


async def un_punisher(ev: SigmaEvent):
    global unpun_loop_running
    if not unpun_loop_running:
        unpun_loop_running = True
        ev.bot.loop.create_task(un_punisher_clock(ev))


async def unban(ev: SigmaEvent, doc: dict):
    try:
        gid = doc.get('ServerID')
        uid = doc.get('UserID')
        guild = discord.utils.find(lambda g: g.id == gid, ev.bot.guilds)
        if guild:
            banlist = await guild.bans()
            target = discord.utils.find(lambda u: u.user.id == uid, banlist)
            if target:
                ev.log.info(f'Un-banning {uid} from {gid}.')
                await guild.unban(target.user, reason='Ban timer ran out.')
    except Exception:
        pass


async def untmute(ev: SigmaEvent, doc: dict):
    try:
        gid = doc.get('ServerID')
        uid = doc.get('UserID')
        guild = discord.utils.find(lambda g: g.id == gid, ev.bot.guilds)
        mutes = await ev.db.get_guild_settings(guild.id, 'MutedUsers') or []
        if uid in mutes:
            ev.log.info(f'Un-muting {uid} from {gid}.')
            mutes.remove(uid)
            await ev.db.set_guild_settings(guild.id, 'MutedUsers', mutes)
    except Exception:
        pass


async def unhmute(ev: SigmaEvent, doc: dict):
    try:
        gid = doc.get('ServerID')
        uid = doc.get('UserID')
        guild = discord.utils.find(lambda g: g.id == gid, ev.bot.guilds)
        if guild:
            target = discord.utils.find(lambda u: u.id == uid, guild.members)
            if target:
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.CategoryChannel):
                        try:
                            ev.log.info(f'Un-hardmuting {uid} from {gid}.')
                            await channel.set_permissions(target, overwrite=None, reason='Hardmute timer ran out.')
                        except discord.Forbidden:
                            pass
    except Exception:
        pass


async def un_punisher_clock(ev: SigmaEvent):
    bancoll = ev.db[ev.db.db_nam].BanClockworkDocs
    tmutecoll = ev.db[ev.db.db_nam].TextmuteClockworkDocs
    hmutecoll = ev.db[ev.db.db_nam].HardmuteClockworkDocs
    while True:
        if ev.bot.is_ready:
            now = arrow.utcnow().timestamp
            lookup = {'Time': {'$lt': now}}
            banned = await bancoll.find_one_and_delete(lookup)
            if banned:
                await unban(ev, banned)
            tmuted = await tmutecoll.find_one_and_delete(lookup)
            if tmuted:
                await untmute(ev, tmuted)
            hmuted = await hmutecoll.find_one_and_delete(lookup)
            if hmuted:
                await unhmute(ev, hmuted)
        await asyncio.sleep(1)
