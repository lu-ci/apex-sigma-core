# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


async def blockwords(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            blocked_words = await cmd.db.get_guild_settings(message.guild.id, 'BlockedWords')
            if blocked_words is None:
                blocked_words = []
            added_words = []
            for word in args:
                if word.lower() not in blocked_words:
                    blocked_words.append(word.lower())
                    added_words.append(word.lower())
            await cmd.db.set_guild_settings(message.guild.id, 'BlockedWords', blocked_words)
            if added_words:
                color = 0x66CC66
                title = f'✅ I have added {len(added_words)} to the blacklist.'
            else:
                color = 0x3B88C3
                title = 'ℹ No new words were added.'
            response = discord.Embed(color=color, title=title)
        else:
            response = discord.Embed(title='⛔ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
