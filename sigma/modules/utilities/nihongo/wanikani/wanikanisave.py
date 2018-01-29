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


async def wanikanisave(cmd, message, args):
    try:
        await message.delete()
    except discord.ClientException:
        pass
    if args:
        api_key = ''.join(args)
        api_document = await cmd.db[cmd.db.db_cfg.database]['WaniKani'].find_one({'UserID': message.author.id})
        data = {'UserID': message.author.id, 'WKAPIKey': api_key}
        if api_document:
            ender = 'updated'
            await cmd.db[cmd.db.db_cfg.database]['WaniKani'].update_one({'UserID': message.author.id}, {'$set': data})
        else:
            ender = 'saved'
            await cmd.db[cmd.db.db_cfg.database]['WaniKani'].insert_one(data)
        response = discord.Embed(color=0x66CC66, title=f'🔑 Your key has been {ender}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
