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


async def greetdm(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        out_content = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Manage Server needed.')
    else:
        active = await cmd.db.get_guild_settings(message.guild.id, 'GreetDM')
        if active:
            await cmd.db.set_guild_settings(message.guild.id, 'GreetDM', False)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been disabled.')
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'GreetDM', True)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been enabled.')
    await message.channel.send(None, embed=out_content)
