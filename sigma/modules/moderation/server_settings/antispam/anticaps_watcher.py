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

import string

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


def count_chars(text):
    """

    :param text:
    :type text:
    :return:
    :rtype:
    """
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


async def anticaps_watcher(ev: SigmaEvent, pld: MessagePayload):
    """

    :param ev:
    :type ev:
    :param pld:
    :type pld:
    """
    if pld.msg.guild and pld.msg.author:
        if isinstance(pld.msg.author, discord.Member):
            is_owner = pld.msg.author.id in ev.bot.cfg.dsc.owners
            if not pld.msg.author.guild_permissions.administrator or not is_owner:
                if pld.msg.content:
                    anticaps = pld.settings.get('anticaps')
                    if anticaps:
                        cap_limit = pld.settings.get('caps_limit') or 5
                        cap_percent = pld.settings.get('caps_percentage') or 60
                        total, upper, percent = count_chars(pld.msg.content)
                        if upper >= cap_limit and percent >= cap_percent:
                            await pld.msg.delete()
                            title = '📢 Anticaps: Removed a message.'
                            user = f'User: {pld.msg.author.id}'
                            channel = f'Channel: {pld.msg.channel.name}'
                            stats = f'Caps: {upper}/{total} {percent}%'
                            log_embed = discord.Embed(color=0xdd2e44, title=title)
                            log_embed.set_author(name=f'{pld.msg.author.name}', icon_url=user_avatar(pld.msg.author))
                            log_embed.description = pld.msg.content
                            log_embed.set_footer(text=f'{user} | {channel} | {stats}')
                            await log_event(ev.bot, pld.settings, log_embed, 'log_antispam')
