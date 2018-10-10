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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


def settings(args: list):
    private = False
    locked = False
    for arg in args:
        if arg.lower() == 'private':
            private = True
        if arg.lower() == 'locked':
            locked = True
    return private, locked


async def makelist(cmd: SigmaCommand, message: discord.Message, args: list):
    private = False
    locked = False
    if args:
        private, locked = settings(args)
    list_data = {
        'server_id': message.guild.id,
        'user_id': message.author.id,
        'list_id': secrets.token_hex(2),
        'private': private,
        'locked': locked,
        'contents': []
    }
    await cmd.db[cmd.db.db_nam].CustomLists.insert_one(list_data)
    response = discord.Embed(color=0x77B255)
    response.title = f'✅ List `{list_data.get("list_id")}` has been created.'
    await message.channel.send(embed=response)
