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


def is_invalid(name):
    invalid = False
    for char in name:
        if char not in string.printable:
            invalid = True
            break
    return invalid


def clean_name(name, default):
    end_name = ''
    for char in name:
        if char in string.printable:
            end_name += char
    if not end_name:
        end_name = default
    return end_name


async def edit_name_check(ev: SigmaEvent, before: discord.Member, after: discord.Member):
    if after.guild:
        if before.display_name != after.display_name:
            active = await ev.db.get_guild_settings(after.guild.id, 'ascii_only_names')
            if active:
                if is_invalid(after.display_name):
                    try:
                        temp_name = await ev.db.get_guild_settings(after.guild.id, 'ascii_temp_name')
                        new_name = clean_name(after.display_name, temp_name)
                        await after.edit(nick=new_name, reason='ASCII name enforcement.')
                    except Exception:
                        pass
