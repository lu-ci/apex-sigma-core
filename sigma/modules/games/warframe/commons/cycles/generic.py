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

import arrow

from sigma.core.mechanics.database import Database
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import GuildPayload


async def get_channels(ev: SigmaEvent, marker):
    """

    :param ev:
    :type ev:
    :param marker:
    :type marker:
    :return:
    :rtype:
    """
    channel_list = []
    lookup = {marker: {'$exists': True}}
    setting_files = await ev.db[ev.db.db_nam].ServerSettings.find(lookup).to_list(None)
    for setting_file in setting_files:
        channel_id = setting_file.get(marker)
        channel = await ev.bot.get_channel(channel_id, True)
        if channel:
            perms = channel.permissions_for(channel.guild.me)
            if perms.send_messages and perms.embed_links:
                channel_list.append(channel)
    return channel_list


async def get_triggers(db, triggers, pld: GuildPayload):
    """

    :param db:
    :type db:
    :param triggers:
    :type triggers:
    :param pld:
    :type pld:
    :return:
    :rtype:
    """
    mentions = []
    for trigger in triggers:
        wf_tags = await db.get_guild_settings(pld.guild.id, 'warframe_tags')
        if wf_tags is None:
            wf_tags = {}
        if wf_tags:
            if trigger in wf_tags:
                role_id = wf_tags.get(trigger)
                bound_role = pld.guild.get_role(role_id)
                if bound_role:
                    mentions.append(bound_role.mention)
    return mentions


async def clean_wf_cache(db: Database):
    """

    :param db:
    :type db:
    """
    cutoff = arrow.utcnow().timestamp - 2592000
    await db[db.db_nam].WarframeCache.delete_many({'created': {'$lt': cutoff}})


async def send_to_channels(ev: SigmaEvent, response, marker, triggers=None):
    """

    :param ev:
    :type ev:
    :param response:
    :type response:
    :param marker:
    :type marker:
    :param triggers:
    :type triggers:
    """
    channels = await get_channels(ev, marker)
    for channel in channels:
        # noinspection PyBroadException
        try:
            if triggers:
                mentions = await get_triggers(ev.db, triggers, channel)
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
