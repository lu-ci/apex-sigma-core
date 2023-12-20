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

import secrets

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


def make_sugg_data(msg, args, token):
    """
    :type msg: discord.Message
    :type args: list
    :type token: str
    :rtype: dict
    """
    return {
        'suggestion': {
            'id': token,
            'text': ' '.join(args)
        },
        'user': {
            'id': msg.author.id,
            'name': msg.author.name,
            'color': msg.author.color.value,
            'avatar': user_avatar(msg.author)
        },
        'guild': {
            'id': msg.guild.id,
            'name': msg.guild.name,
            'icon': str(msg.guild.icon.url) if msg.guild.icon else None
        },
        'timestamp': msg.created_at.timestamp(),
        'reported': False
    }


async def botsuggest(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    coll = cmd.db[cmd.db.db_name].Suggestions
    if cmd.cfg.channel:
        if pld.args:
            sugg_text = ' '.join(pld.args)
            exmp_text = ' '.join(cmd.usage.split(' ')[1:])
            if sugg_text.lower() != exmp_text.lower():
                sugg_token = secrets.token_hex(4)
                await coll.insert_one(make_sugg_data(pld.msg, pld.args, sugg_token))
                response = GenericResponse(f'Suggestion {sugg_token} submitted.').ok()
            else:
                response = GenericResponse('Please do not use this command to submit the usage example.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Missing suggestion channel configuration.').error()
    await pld.msg.channel.send(embed=response)
