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

from sigma.core.utilities.generic_responses import ok
from sigma.modules.minigames.utils.ongoing.ongoing import ongoing_storage


async def resetongoing(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    for identifier in [pld.msg.author.id, pld.msg.channel.id, pld.msg.guild.id]:
        for key in ongoing_storage:
            ongoing_list = ongoing_storage.get(key) or []
            if identifier in ongoing_list:
                ongoing_list.remove(identifier)
            ongoing_storage.update({key: ongoing_list})
    response = ok('Ongoing user, channel and guild locks cleared.')
    await pld.msg.channel.send(embed=response)
