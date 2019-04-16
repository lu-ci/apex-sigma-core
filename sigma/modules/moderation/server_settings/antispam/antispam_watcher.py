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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


async def rate_limited(db, msg, amt, tsp):
    """
    Chceks if the sent message was subject to rate limiting.
    :param db: The main database handler instance.
    :type db: sigma.core.mechanics.database.Database
    :param msg: The message that was sent.
    :type msg: discord.Message
    :param amt: Maximum amount to send in the timespan.
    :type amt: int
    :param tsp: The timespan in which the messages are subjecto limitations.
    :type tsp: int
    :return:
    :rtype: bool
    """
    limit_key = f'{msg.guild.id}_{msg.author.id}'
    cache_key = f'rate_limit_{limit_key}'
    limit_items = await db.cache.get_cache(cache_key) or []
    limit_items.append(msg)
    for lit in limit_items:
        if lit.created_at.timestamp() < limit_items[-1].created_at.timestamp() - tsp:
            limit_items.remove(lit)
    await db.cache.set_cache(cache_key, limit_items)
    return len(limit_items) > amt


async def antispam_watcher(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.guild and pld.msg.author:
        if isinstance(pld.msg.author, discord.Member):
            is_owner = pld.msg.author.id in ev.bot.cfg.dsc.owners
            if not pld.msg.author.guild_permissions.administrator or not is_owner:
                if pld.msg.content:
                    antispam = pld.settings.get('antispam')
                    if antispam:
                        amount = pld.settings.get('rate_limit_amount') or 5
                        timespan = pld.settings.get('rate_limit_timespan') or 5
                        if await rate_limited(ev.db, pld.msg, amount, timespan):
                            await pld.msg.delete()
                            title = '📢 Antispam: Removed a message.'
                            user = f'User: {pld.msg.author.id}'
                            channel = f'Channel: {pld.msg.channel.name}'
                            log_embed = discord.Embed(color=0xdd2e44, title=title)
                            log_embed.set_author(name=f'{pld.msg.author.name}', icon_url=user_avatar(pld.msg.author))
                            log_embed.description = pld.msg.content
                            log_embed.set_footer(text=f'{user} | {channel}')
                            await log_event(ev.bot, pld.settings, log_embed, 'log_antispam')
