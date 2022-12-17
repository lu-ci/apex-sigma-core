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
from sigma.modules.utilities.mathematics.collector_clockwork import current_doc_collecting


async def cancelcollector(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    collector_coll = cmd.db[cmd.db.db_nam].CollectorQueue
    current_target = current_doc_collecting.get('user_id')
    current_author = current_doc_collecting.get('author_id')
    if pld.msg.author.id not in [current_target, current_author]:
        target_entry = await collector_coll.find_one({'user_id': pld.msg.author.id})
        author_entry = await collector_coll.find_one({'author_id': pld.msg.author.id})
        entry = target_entry or author_entry
        if entry:
            await collector_coll.delete_one(entry)
            response = GenericResponse('Ok, I removed you from the queue.').ok()
        else:
            response = GenericResponse('You are not currently in the queue.').error()
    else:
        response = GenericResponse('Can\'t cancel an already ongoing collection.').error()
    await pld.msg.channel.send(embed=response)
