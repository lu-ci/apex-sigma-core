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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, ok


def make_sugg_data(msg: discord.Message, args: list, token: str):
    """

    :param msg:
    :type msg:
    :param args:
    :type args:
    :param token:
    :type token:
    :return:
    :rtype:
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
            'icon': str(msg.guild.icon_url) if msg.guild.icon_url else None
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
    coll = cmd.db[cmd.db.db_nam].Suggestions
    if cmd.cfg.channel:
        if pld.args:
            sugg_text = ' '.join(pld.args)
            exmp_text = ' '.join(cmd.usage.split(' ')[1:])
            if sugg_text.lower() != exmp_text.lower():
                sugg_token = secrets.token_hex(4)
                await coll.insert_one(make_sugg_data(pld.msg, pld.args, sugg_token))
                response = ok(f'Suggestion {sugg_token} submitted.')
            else:
                response = error('Please do not use this command to submit the usage example.')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('Missing suggestion channel configuration.')
    await pld.msg.channel.send(embed=response)
