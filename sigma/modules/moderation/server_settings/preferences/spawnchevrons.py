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
from sigma.core.utilities.generic_responses import permission_denied


async def spawnchevrons(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_guild:
        humans = len([x for x in message.guild.members if not x.bot])
        if humans >= 50:
            target = message.channel_mentions[0] if message.channel_mentions else message.channel
            chev_chns = await cmd.db.get_guild_settings(message.guild.id, 'chevron_channels') or []
            if target.id not in chev_chns:
                chev_chns.append(target.id)
                response = discord.Embed(color=0x77B255, title=f'✅ Chevron spawning enabled in #{target.name}.')
            else:
                chev_chns.remove(target.id)
                response = discord.Embed(color=0x77B255, title=f'✅ Chevron spawning disabled in #{target.name}.')
            await cmd.db.set_guild_settings(message.guild.id, 'chevron_channels', chev_chns)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {message.guild.name} does not have enough humans.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
