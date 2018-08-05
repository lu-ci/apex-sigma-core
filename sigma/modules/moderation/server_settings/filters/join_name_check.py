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
from sigma.modules.moderation.server_settings.filters.edit_name_check import is_invalid, clean_name


async def join_name_check(ev: SigmaEvent, member: discord.Member):
    if member.guild:
        active = await ev.db.get_guild_settings(member.guild.id, 'ascii_only_names')
        if active:
            if is_invalid(member.display_name):
                try:
                    temp_name = await ev.db.get_guild_settings(member.guild.id, 'ascii_temp_name')
                    new_name = clean_name(member.display_name, temp_name)
                    await member.edit(nick=new_name, reason='ASCII name enforcement.')
                except Exception:
                    pass
