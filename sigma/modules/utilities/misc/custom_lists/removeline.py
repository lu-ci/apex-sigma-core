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

from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.utilities.misc.custom_lists.addline import user_auth


async def removeline(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.args) > 1:
        list_coll = cmd.db[cmd.db.db_nam].CustomLists
        lookup_data = {'server_id': pld.msg.guild.id, 'list_id': pld.args[0].lower()}
        list_file = await list_coll.find_one(lookup_data)
        if list_file:
            if user_auth(pld.msg, list_file):
                line = pld.args[1]
                if line.isdigit():
                    try:
                        line_num = max(1, int(line))
                        list_file.get('contents', []).pop(line_num - 1)
                        await list_coll.update_one(lookup_data, {'$set': list_file})
                        response = discord.Embed(color=0xFFCC4D, title=f'🔥 Line {line_num} was deleted.')
                    except IndexError:
                        response = not_found('Line not found.')
                else:
                    response = error('Invalid line number.')
            else:
                mode = 'private' if list_file.get('mode') == 'private' else 'locked'
                response = discord.Embed(color=0xFFAC33, title=f'🔏 This list is {mode}.')
        else:
            response = error('Missing or invalid list ID.')
    else:
        response = error('Not enough arguments.')
    await pld.msg.channel.send(embed=response)
