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
from sigma.modules.utilities.misc.afk.afk import afk_cache


async def afk_comeback_check(ev: SigmaEvent, message: discord.Message):
    if message.guild:
        pfx = await ev.db.get_prefix(message)
        if not message.content.startswith(pfx):
            afk_data = afk_cache.get_cache(message.author.id)
            if not afk_data:
                afk_data = await ev.db[ev.db.db_nam].AwayUsers.find_one_and_delete({'user_id': message.author.id})
            if afk_data:
                afk_cache.del_cache(message.author.id)
                response = discord.Embed(color=0x3B88C3, title='ℹ I have removed your AFK status.')
                removal = await message.channel.send(embed=response)
                await asyncio.sleep(5)
                try:
                    await removal.delete()
                except discord.ClientException:
                    pass
