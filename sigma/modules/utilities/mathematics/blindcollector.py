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


async def blindcollector(cmd: SigmaCommand, message: discord.Message, _args: list):
    if message.author.guild_permissions.manage_channels:
        if message.channel_mentions:
            target = message.channel_mentions[0]
            docdata = {'channel_id': target.id}
            blockdoc = bool(await cmd.db[cmd.db.db_nam].BlindedChains.find_one(docdata))
            if blockdoc:
                await cmd.db[cmd.db.db_nam].BlindedChains.delete_one(docdata)
                response_title = f'✅ Users can once again collect chains from #{target.name}.'
            else:
                await cmd.db[cmd.db.db_nam].BlindedChains.insert_one(docdata)
                response_title = f'✅ Users can no longer collect chains from #{target.name}.'
            response = discord.Embed(color=0x66CC66, title=response_title)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No channel given.')
    else:
        response = permission_denied('Manage Channels')
    await message.channel.send(embed=response)
