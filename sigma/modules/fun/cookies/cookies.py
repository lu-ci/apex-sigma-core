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


async def cookies(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    cookie_coll = cmd.db[cmd.db.db_cfg.database].Cookies
    cookie_file = await cookie_coll.find_one({'UserID': target.id})
    if cookie_file:
        cookie_count = cookie_file['Cookies']
    else:
        cookie_count = 0
    if cookie_count == 1:
        ender = 'cookie'
    else:
        ender = 'cookies'
    title = f'🍪 {target.display_name} has {cookie_count} {ender}.'
    response = discord.Embed(color=0xd99e82, title=title)
    await message.channel.send(embed=response)
