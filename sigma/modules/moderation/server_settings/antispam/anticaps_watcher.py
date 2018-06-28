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

import string

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


def count_chars(text):
    upper = 0
    lower = 0
    for c in text:
        if c not in string.whitespace:
            if c.isupper():
                upper += 1
            else:
                lower += 1
    total = upper + lower
    percent = int(upper / total * 100)
    return total, upper, percent


async def anticaps_watcher(ev: SigmaEvent, message: discord.Message):
    if message.guild and message.author:
        if message.author.guild_permissions.administrator and message.author.id not in ev.bot.cfg.dsc.owners:
            if message.content:
                anticaps = await ev.db.get_guild_settings(message.guild.id, 'AntiCaps')
                if anticaps:
                    cap_limit = await ev.db.get_guild_settings(message.guild.id, 'CapsLimit') or 5
                    cap_percent = await ev.db.get_guild_settings(message.guild.id, 'CapsPercentage') or 60
                    total, upper, percent = count_chars(message.content)
                    if upper >= cap_limit and percent >= cap_percent:
                        await message.delete()
                        title = f'📢 Anticaps: Removed a message.'
                        user = f'User: {message.author.id}'
                        channel = f'Channel: {message.channel.name}'
                        stats = f'Caps: {upper}/{total} {percent}%'
                        log_embed = discord.Embed(color=0xdd2e44, title=title)
                        log_embed.set_author(name=f'{message.author.name}', icon_url=user_avatar(message.author))
                        log_embed.description = message.content
                        log_embed.set_footer(text=f'{user} | {channel} | {stats}')
                        await log_event(ev.bot, message.guild, ev.db, log_embed, 'LogAntispam')
