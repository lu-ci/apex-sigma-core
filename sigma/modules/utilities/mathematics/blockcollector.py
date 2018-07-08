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


async def blockcollector(cmd: SigmaCommand, message: discord.Message, args: list):
    block_data = {'UserID': message.author.id}
    block_coll = cmd.db[cmd.db.db_nam].BlockedChains
    block_file = await block_coll.find_one(block_data)
    if not block_file:
        await block_coll.insert_one(block_data)
        response_title = '✅ Other users are no longer able to collect a chain for you.'
    else:
        await block_coll.delete_one(block_data)
        response_title = '✅ Other users can once again collect a chain for you.'
    response = discord.Embed(color=0x66CC66, title=response_title)
    await message.channel.send(embed=response)
