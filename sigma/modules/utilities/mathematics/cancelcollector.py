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
from sigma.core.utilities.generic_responses import ok, error
from sigma.modules.utilities.mathematics.collector_clockwork import current_user_collecting


async def cancelcollector(cmd: SigmaCommand, pld: CommandPayload):
    collector_coll = cmd.db[cmd.db.db_nam].CollectorQueue
    current = current_user_collecting
    if pld.msg.author.id != current:
        entry = await collector_coll.find_one({'user_id': pld.msg.author.id})
        if entry:
            await collector_coll.delete_one(entry)
            response = ok('Ok, I removed you from the queue.')
        else:
            response = error('You are not currently in the queue.')
    else:
        response = error('Can\'t cancel a already ongoing collection.')
    await pld.msg.channel.send(embed=response)
