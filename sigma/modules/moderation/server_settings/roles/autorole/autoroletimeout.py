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

from sigma.core.mechanics.command import SigmaCommand


async def autoroletimeout(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            try:
                timeout = abs(int(args[0]))
            except ValueError:
                timeout = None
            if timeout is not None:
                await cmd.db.set_guild_settings(message.guild.id, 'AutoroleTimeout', timeout)
                response = discord.Embed(color=0x77B255, title=f'✅ Timeout set to {timeout} seconds.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
        else:
            timeout = await cmd.db.get_guild_settings(message.guild.id, 'AutoroleTimeout') or 0
            response = discord.Embed(color=0x696969, title=f'🕙 The current timeout is {timeout} seconds.')
    else:
        response = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Manage Server needed.')
    await message.channel.send(embed=response)
