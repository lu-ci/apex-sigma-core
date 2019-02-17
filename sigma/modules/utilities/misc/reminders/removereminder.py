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
from sigma.core.utilities.generic_responses import error, not_found, ok


async def removereminder(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        rem_id = pld.args[0].lower()
        lookup_data = {'user_id': pld.msg.author.id, 'reminder_id': rem_id}
        reminder = await cmd.db[cmd.db.db_nam].Reminders.find_one(lookup_data)
        if reminder:
            await cmd.db[cmd.db.db_nam].Reminders.delete_one(lookup_data)
            response = ok(f'Reminder {rem_id} has been deleted.')
        else:
            response = not_found(f'Reminder `{rem_id}` not found.')
    else:
        response = error('Missing reminder ID.')
    await pld.msg.channel.send(embed=response)
