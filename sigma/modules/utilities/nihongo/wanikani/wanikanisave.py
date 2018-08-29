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


async def wanikanisave(cmd: SigmaCommand, message: discord.Message, args: list):
    try:
        await message.delete()
    except (discord.NotFound, discord.Forbidden):
        pass
    if args:
        api_key = ''.join(args)
        api_document = await cmd.db[cmd.db.db_nam].WaniKani.find_one({'user_id': message.author.id})
        data = {'user_id': message.author.id, 'wk_api_key': api_key}
        if api_document:
            ender = 'updated'
            await cmd.db[cmd.db.db_nam].WaniKani.update_one({'user_id': message.author.id}, {'$set': data})
        else:
            ender = 'saved'
            await cmd.db[cmd.db.db_nam].WaniKani.insert_one(data)
        response = discord.Embed(color=0x66CC66, title=f'🔑 Your key has been {ender}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
