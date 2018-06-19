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
import string

import discord

from sigma.core.mechanics.event import SigmaEvent

cleaner_loop_running = False


def clean_name(name, default):
    end_name = ''
    for char in name:
        if char in string.printable:
            end_name += char
    if not end_name:
        end_name = default
    return end_name


async def name_check_clockwork(ev: SigmaEvent):
    global cleaner_loop_running
    if not cleaner_loop_running:
        cleaner_loop_running = True
        ev.bot.loop.create_task(name_checker(ev))


async def name_checker(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            guild_ids = []
            guilds = []
            actives = await ev.db[ev.db.db_cfg.database].ServerSettings.find({'ASCIIOnlyNames': True}).to_list(None)
            for doc in actives:
                gid = doc['ServerID']
                guild_ids.append(gid)
            for guild_id in guild_ids:
                active_guild = discord.utils.find(lambda x: x.id == guild_id, ev.bot.guilds)
                if active_guild:
                    guilds.append(active_guild)
            for guild in guilds:
                temp_name = await ev.db.get_guild_settings(guild.id, 'ASCIIOnlyTempName')
                if temp_name is None:
                    temp_name = '<ChangeMyName>'
                members = guild.members
                for member in members:
                    nam = member.display_name
                    invalid = False
                    for char in nam:
                        if char not in string.printable:
                            invalid = True
                            break
                    if invalid:
                        try:
                            new_name = clean_name(nam, temp_name)
                            await member.edit(nick=new_name, reason='ASCII name enforcement.')
                        except Exception:
                            pass
        await asyncio.sleep(60)
