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


async def wipechain(cmd: SigmaCommand, pld: CommandPayload):
    uid = message.author.id
    exist_check = await cmd.db[cmd.db.db_nam].MarkovChains.find_one({'user_id': uid})
    if exist_check:
        chain_len = len(exist_check['chain'])
        await cmd.db[cmd.db.db_nam].MarkovChains.delete_one({'user_id': uid})
        response = discord.Embed(color=0x66CC66, title=f'✅ Your chain of {chain_len} items has been wiped.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You don\'t have a Markov Chain.')
    await message.channel.send(embed=response)
