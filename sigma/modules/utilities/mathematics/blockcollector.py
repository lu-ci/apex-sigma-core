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


from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import ok


async def blockcollector(cmd: SigmaCommand, pld: CommandPayload):
    block_data = {'user_id': pld.msg.author.id}
    block_coll = cmd.db[cmd.db.db_nam].BlockedChains
    block_file = await block_coll.find_one(block_data)
    if not block_file:
        await block_coll.insert_one(block_data)
        response = ok('Other users are no longer able to collect a chain for you.')
    else:
        await block_coll.delete_one(block_data)
        response = ok('Other users can once again collect a chain for you.')
    await pld.msg.channel.send(embed=response)
