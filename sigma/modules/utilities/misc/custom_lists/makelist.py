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

from sigma.core.utilities.generic_responses import GenericResponse


def settings(lookup):
    """

    :param lookup:
    :type lookup: str
    :return:
    :rtype: str
    """
    mode = None
    if lookup in ['private', 'locked']:
        mode = lookup
    return mode


async def makelist(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    mode = None
    if pld.args:
        mode = settings(pld.args[0].lower())
    list_data = {
        'server_id': pld.msg.guild.id,
        'user_id': pld.msg.author.id,
        'list_id': secrets.token_hex(2),
        'mode': mode,
        'name': f'{pld.msg.author.name}\'s List',
        'contents': []
    }
    await cmd.db[cmd.db.db_nam].CustomLists.insert_one(list_data)
    response = GenericResponse(f'List `{list_data.get("list_id")}` has been created.').ok()
    response.set_footer(text=f'You can rename it with {cmd.bot.cfg.pref.prefix}renamelist.')
    await pld.msg.channel.send(embed=response)
