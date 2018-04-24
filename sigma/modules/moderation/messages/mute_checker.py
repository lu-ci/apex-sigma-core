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


async def mute_checker(ev: SigmaEvent, message: discord.Message):
    if message.guild:
        if isinstance(message.author, discord.Member):
            if message.author.id not in ev.bot.cfg.dsc.owners:
                if not message.author.permissions_in(message.channel).administrator:
                    mute_list = await ev.db.get_guild_settings(message.guild.id, 'MutedUsers')
                    if mute_list is None:
                        mute_list = []
                    if message.author.id in mute_list:
                        try:
                            await message.delete()
                        except discord.Forbidden:
                            pass
                        except discord.NotFound:
                            pass
