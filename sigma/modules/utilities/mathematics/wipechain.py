# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
from sigma.core.utilities.generic_responses import error, ok


async def wipechain(cmd: SigmaCommand, pld: CommandPayload):
    uid = pld.msg.author.id
    exist_check = await cmd.db[cmd.db.db_nam].MarkovChains.find_one({'user_id': uid})
    if exist_check:
        chain_len = len(exist_check['chain'])
        await cmd.db[cmd.db.db_nam].MarkovChains.delete_one({'user_id': uid})
        response = ok(f'Your chain of {chain_len} items has been wiped.')
    else:
        response = error('You don\'t have a Markov Chain.')
    await pld.msg.channel.send(embed=response)
