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

import arrow

from sigma.core.utilities.generic_responses import error, ok


def generate_data(message, poll_args):
    """

    :param message:
    :type message:
    :param poll_args:
    :type poll_args:
    :return:
    :rtype:
    """
    uid = message.author.id
    if message.channel:
        cid = message.channel.id
    else:
        cid = None
    if message.guild:
        sid = message.guild.id
    else:
        sid = None
    poll_file_data = {
        'id': secrets.token_hex(3),
        'created': arrow.utcnow().float_timestamp,
        'origin': {
            'author': uid,
            'channel': cid,
            'server': sid
        },
        'poll': {
            'question': poll_args[0],
            'answers': poll_args[1:]
        },
        'votes': {},
        'permissions': {
            'channels': [],
            'users': [],
            'roles': []
        },
        'settings': {
            'visible': False,
            'expires': None,
            'active': True
        }
    }
    return poll_file_data


async def shadowpoll(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        poll_args = ' '.join(pld.args).split('; ')
        if len(poll_args) >= 3:
            poll_data = generate_data(pld.msg, poll_args)
            await cmd.db[cmd.db.db_nam].ShadowPolls.insert_one(poll_data)
            response = ok(f'Shadowpoll `{poll_data["id"]}` has been created.')
        else:
            response = error('Not enough arguments.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
