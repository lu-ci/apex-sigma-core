"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.mathematics.collector_clockwork import get_current, cancel_current


async def cancelcollector(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    current = get_current()
    collector_coll = cmd.db[cmd.db.db_nam].CollectorQueue
    if current:
        current_target = current.get('user_id')
        current_author = current.get('author_id')
        current_running = (current_target or current_author) is not None
    else:
        current_running = False
    if not current_running:
        target_entry = await collector_coll.find_one({'user_id': pld.msg.author.id})
        author_entry = await collector_coll.find_one({'author_id': pld.msg.author.id})
        entry = target_entry or author_entry
        if entry:
            await collector_coll.delete_one(entry)
            response = GenericResponse('Ok, I removed you from the queue.').ok()
        else:
            response = GenericResponse('You are not currently in the queue.').error()
    else:
        cancel_current()
        response = GenericResponse('Cancelling your ongoing collection.').error()
    await pld.msg.channel.send(embed=response)
