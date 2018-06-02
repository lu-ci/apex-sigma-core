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


async def byechannel(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = permission_denied('Manage Server')
    else:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
        elif not message.channel_mentions and args:
            channel_name = ' '.join(args).lower()
            target_channel = discord.utils.find(lambda x: x.name.lower() == channel_name, message.guild.channels)
        else:
            target_channel = None
        if target_channel:
            if message.guild.me.permissions_in(target_channel).send_messages:
                await cmd.db.set_guild_settings(message.guild.id, 'ByeChannel', target_channel.id)
                response = discord.Embed(color=0x77B255, title=f'✅ Goodbye Channel set to {target_channel.name}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t write in that channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No channel targeted.')
    await message.channel.send(None, embed=response)
