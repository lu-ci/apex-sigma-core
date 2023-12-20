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
from sigma.modules.development.suggestions.approvesuggestion import react_to_suggestion


async def declinesuggestion(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.args) >= 2:
        token = pld.args[0].lower()
        reason = ' '.join(pld.args[1:])
        suggestion = await cmd.db[cmd.db.db_name].Suggestions.find_one({'suggestion.id': token})
        if suggestion:
            delete = True if reason.lower().startswith('deleted') else False
            await react_to_suggestion(cmd.bot, suggestion, '⛔', delete)
            athr = await cmd.bot.get_user(suggestion.get('user', {}).get('id'))
            if athr:
                to_user = GenericResponse(f'Suggestion {token} declined by {pld.msg.author.display_name}.').denied()
                to_user.description = reason
                try:
                    await athr.send(embed=to_user)
                    response = GenericResponse(f'Suggestion {token} declined.').ok()
                except (discord.Forbidden, discord.NotFound):
                    response = GenericResponse(f'Suggestion {token} declined, but delivery to author failed.').ok()
            else:
                response = GenericResponse(f'Suggestion {token} declined, but the author was not found.').ok()
        else:
            response = GenericResponse('No suggestion entry with that ID was found.').error()
    else:
        response = GenericResponse('Not enough arguments.').error()
    await pld.msg.channel.send(embed=response)
