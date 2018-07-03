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

from sigma.core.mechanics.database import Database
from sigma.core.mechanics.event import SigmaEvent


async def get_channels(ev: SigmaEvent, marker):
    all_channels = ev.bot.get_all_channels()
    channel_list = []
    lookup = {marker: {'$exists': True}}
    setting_files = await ev.db[ev.db.db_cfg.database].ServerSettings.find(lookup).to_list(None)
    for setting_file in setting_files:
        channel_id = setting_file.get(marker)
        channel = discord.utils.find(lambda x: x.id == channel_id, all_channels)
        if channel:
            perms = channel.permissions_for(channel.guild.me)
            if perms.send_messages and perms.embed_links:
                channel_list.append(channel)
    return channel_list


async def get_triggers(db, triggers, guild):
    mentions = []
    for trigger in triggers:
        wf_tags = await db.get_guild_settings(guild.id, 'WarframeTags')
        if wf_tags is None:
            wf_tags = {}
        if wf_tags:
            if trigger in wf_tags:
                role_id = wf_tags.get(trigger)
                bound_role = discord.utils.find(lambda x: x.id == role_id, guild.roles)
                if bound_role:
                    mentions.append(bound_role.mention)
    return mentions


async def clean_wf_cache(db: Database):
    cutoff = arrow.utcnow().timestamp - 86500
    await db[db.db_cfg.database].WarframeCache.delete_many({'Created': {'$lt': cutoff}})


async def send_to_channels(ev: SigmaEvent, response, marker, triggers=None):
    channels = await get_channels(ev, marker)
    for channel in channels:
        try:
            if triggers:
                mentions = await get_triggers(ev.db, triggers, channel.guild)
                if mentions:
                    mentions = ' '.join(mentions)
                    await channel.send(mentions, embed=response)
                else:
                    await channel.send(embed=response)
            else:
                await channel.send(embed=response)
            await asyncio.sleep(2.5)
        except Exception:
            pass
    await clean_wf_cache(ev.db)
