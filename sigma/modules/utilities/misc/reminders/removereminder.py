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


async def removereminder(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        rem_id = pld.args[0].lower()
        lookup_data = {'user_id': pld.msg.author.id, 'reminder_id': rem_id}
        reminder = await cmd.db.col.Reminders.find_one(lookup_data)
        if reminder:
            await cmd.db.col.Reminders.delete_one(lookup_data)
            response = GenericResponse(f'Reminder {rem_id} has been deleted.').ok()
        else:
            response = GenericResponse(f'Reminder `{rem_id}` not found.').not_found()
    else:
        response = GenericResponse('Missing reminder ID.').error()
    await pld.msg.channel.send(embed=response)
