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

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event

rate_limit_cache = {}


def rate_limited(msg: discord.Message, amt: int, tsp: int):
    limit_key = f'{msg.guild.id}_{msg.author.id}'
    limit_items = rate_limit_cache.get(limit_key, [])
    limit_items.append(msg)
    for lit in limit_items:
        if lit.created_at.timestamp() < limit_items[-1].created_at.timestamp() - tsp:
            limit_items.remove(lit)
    rate_limit_cache.update({limit_key: limit_items})
    return len(limit_items) > amt


async def antispam_watcher(ev: SigmaEvent, pld: MessagePayload):
    if pld.msg.guild and pld.msg.author:
        if isinstance(pld.msg.author, discord.Member):
            is_owner = pld.msg.author.id in ev.bot.cfg.dsc.owners
            if not pld.msg.author.guild_permissions.administrator or not is_owner:
                if pld.msg.content:
                    antispam = await ev.db.get_guild_settings(pld.msg.guild.id, 'antispam')
                    if antispam:
                        amount = await ev.db.get_guild_settings(pld.msg.guild.id, 'rate_limit_amount') or 5
                        timespan = await ev.db.get_guild_settings(pld.msg.guild.id, 'rate_limit_timespan') or 5
                        if rate_limited(pld.msg, amount, timespan):
                            await pld.msg.delete()
                            title = f'📢 Antispam: Removed a pld.msg.'
                            user = f'User: {pld.msg.author.id}'
                            channel = f'Channel: {pld.msg.channel.name}'
                            log_embed = discord.Embed(color=0xdd2e44, title=title)
                            log_embed.set_author(name=f'{pld.msg.author.name}', icon_url=user_avatar(pld.msg.author))
                            log_embed.description = pld.msg.content
                            log_embed.set_footer(text=f'{user} | {channel}')
                            await log_event(ev.bot, pld.msg.guild, ev.db, log_embed, 'log_antispam')
