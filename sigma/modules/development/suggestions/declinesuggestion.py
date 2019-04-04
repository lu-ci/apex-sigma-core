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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, ok
from sigma.modules.development.suggestions.approvesuggestion import react_to_suggestion


async def declinesuggestion(cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.args) >= 2:
        token = pld.args[0].lower()
        reason = ' '.join(pld.args[1:])
        suggestion = await cmd.db[cmd.db.db_nam].Suggestions.find_one({'suggestion.id': token})
        if suggestion:
            delete = True if reason.lower().startswith('deleted') else False
            await react_to_suggestion(cmd.bot, suggestion, '⛔', delete)
            athr = await cmd.bot.get_user(suggestion.get('user', {}).get('id'))
            if athr:
                to_user = denied(f'Suggestion {token} declined by {pld.msg.author.display_name}.')
                to_user.description = reason
                try:
                    await athr.send(embed=to_user)
                    response = ok(f'Suggestion {token} declined.')
                except (discord.Forbidden, discord.NotFound):
                    response = ok(f'Suggestion {token} declined, but delivery to author failed.')
            else:
                response = ok(f'Suggestion {token} declined, but the author was not found.')
        else:
            response = error('No suggestion entry with that ID was found.')
    else:
        response = error('Not enough arguments.')
    await pld.msg.channel.send(embed=response)
