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


async def endraffle(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        rafid = args[0].lower()
        raffle = await cmd.db[cmd.db.db_nam].Raffles.find_one({'id': rafid, 'active': True})
        if raffle:
            aid = raffle.get('author')
            if aid == message.author.id:
                await cmd.db[cmd.db.db_nam].Raffles.update_one(raffle, {'$set': {'end': 0}})
                reaction = '✅'
            else:
                reaction = '⛔'
        else:
            reaction = '🔍'
    else:
        reaction = '❗'
    await message.add_reaction(reaction)
