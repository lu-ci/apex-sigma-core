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
from sigma.modules.moderation.server_settings.starboard.starboard_watcher import starboard_cache


async def starboardchannel(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if message.channel_mentions:
            target_channel = message.channel_mentions[0]
            if message.guild.me.permissions_in(target_channel).send_messages:
                starboard_doc = await cmd.db.get_guild_settings(message.guild.id, 'starboard') or {}
                starboard_doc.update({'channel_id': target_channel.id})
                await cmd.db.set_guild_settings(message.guild.id, 'starboard', starboard_doc)
                response = discord.Embed(color=0x77B255, title=f'✅ Starboard channel set to {target_channel.name}.')
                starboard_cache.set_cache(message.guild.id, starboard_doc)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t write in that channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No channel targeted.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
