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

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def shadowpollclose(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        poll_id = pld.args[0].lower()
        poll_file = await cmd.db.col.ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == pld.msg.author.id:
                active = poll_file['settings']['active']
                if active:
                    poll_file['settings'].update({'active': False})
                    await cmd.db.col.ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                    response = discord.Embed(color=0xFFCC4D, title=f'🔒 Poll {poll_file["id"]} has been closed.')
                else:
                    response = GenericResponse(f'Poll {poll_file["id"]} is not active.').error()
            else:
                response = GenericResponse('You didn\'t make this poll.').denied()
        else:
            response = GenericResponse('Poll not found.').not_found()
    else:
        response = GenericResponse('Missing poll ID.').error()
    await pld.msg.channel.send(embed=response)
