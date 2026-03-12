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


async def shadowpollpermit(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) >= 2:
            poll_id = pld.args[0].lower()
            if pld.msg.mentions:
                perm_type = 'users'
                target = pld.msg.mentions[0]
            elif pld.msg.channel_mentions:
                perm_type = 'channels'
                target = pld.msg.channel_mentions[0]
            else:
                lookup = ' '.join(pld.args[1:]).lower()
                perm_type = 'roles'
                target = discord.utils.find(lambda x: x.name.lower() == lookup, pld.msg.guild.roles)
            if target:
                poll_file = await cmd.db.col.ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    author = poll_file['origin']['author']
                    if author == pld.msg.author.id:
                        if target.id not in poll_file['permissions'][perm_type]:
                            poll_file['permissions'][perm_type].append(target.id)
                            await cmd.db.col.ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                            response = GenericResponse(f'{target.name} has been permitted.').ok()
                        else:
                            response = GenericResponse(f'{target.name} is already permitted.').error()
                    else:
                        response = GenericResponse('You didn\'t make this poll.').denied()
                else:
                    response = GenericResponse('Poll not found.').not_found()
            else:
                response = GenericResponse('Target not located.').error()
        else:
            response = GenericResponse('Not enough arguments.').error()
    else:
        response = GenericResponse('Missing poll ID and target.').error()
    await pld.msg.channel.send(embed=response)
