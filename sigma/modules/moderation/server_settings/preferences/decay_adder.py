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

import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.modules.moderation.server_settings.preferences.decay_checker import decay_cache


async def decay_adder(ev: SigmaEvent, msg: discord.Message):
    if msg.guild:
        dchns = await ev.db.get_guild_settings(msg.guild.id, 'DecayingChannels') or []
        if msg.channel.id in dchns:
            dtmrs = await ev.db.get_guild_settings(msg.guild.id, 'DecayingTimers') or {}
            dtmr = dtmrs.get(str(msg.channel.id))
            if dtmr:
                deletion_stamp = arrow.utcnow().timestamp + dtmr
                tracking_data = {'Message': msg.id, 'Channel': msg.channel.id, 'Timestamp': deletion_stamp}
                await ev.db[ev.db.db_nam].DecayingMessages.insert_one(tracking_data)
                decay_cache.del_cache('all')
