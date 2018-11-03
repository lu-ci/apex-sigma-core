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

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload


async def afk_comeback_check(ev: SigmaEvent, pld: MessagePayload):
    if pld.msg.guild:
        pfx = ev.db.get_prefix(pld.settings)
        if not pld.msg.content.startswith(pfx):
            afk_data = await ev.db[ev.db.db_nam].AwayUsers.find_one_and_delete({'user_id': pld.msg.author.id})
            if afk_data:
                await ev.db.cache.del_cache(f'afk_{pld.msg.author.id}')
                response = discord.Embed(color=0x3B88C3, title='ℹ I have removed your AFK status.')
                removal = await pld.msg.channel.send(embed=response)
                await asyncio.sleep(5)
                try:
                    await removal.delete()
                except discord.ClientException:
                    pass
