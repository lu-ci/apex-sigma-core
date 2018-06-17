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

from sigma.core.mechanics.database import Database
from sigma.core.sigma import ApexSigma


async def log_event(client: ApexSigma, guild: discord.Guild, db: Database, embed: discord.Embed, event: str):
    all_channels = client.get_all_channels()
    log_channel_id = await db.get_guild_settings(guild.id, f'{event}Channel')
    log_event_active = await db.get_guild_settings(guild.id, event)
    if log_channel_id and log_event_active:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, all_channels)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except Exception:
                pass
