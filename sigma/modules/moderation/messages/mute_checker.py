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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload


async def mute_checker(ev: SigmaEvent, pld: MessagePayload):
    if pld.msg.guild:
        if isinstance(pld.msg.author, discord.Member):
            if pld.msg.author.id not in ev.bot.cfg.dsc.owners:
                if not pld.msg.author.permissions_in(pld.msg.channel).administrator:
                    mute_list = pld.settings.get('muted_users') or []
                    if pld.msg.author.id in mute_list:
                        try:
                            await pld.msg.delete()
                        except discord.Forbidden:
                            pass
                        except discord.NotFound:
                            pass
