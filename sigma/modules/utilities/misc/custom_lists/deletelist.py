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


async def deletelist(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        lookup_data = {'list_id': pld.args[0].lower()}
        list_coll = cmd.db[cmd.db.db_name].CustomLists
        list_file = await list_coll.find_one(lookup_data)
        if list_file:
            author_id = list_file.get('user_id')
            if author_id == pld.msg.author.id:
                await list_coll.delete_one(lookup_data)
                title = f'🔥 List `{list_file.get("list_id")}` has been deleted.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = GenericResponse('You didn\'t make this list.').denied()
        else:
            response = GenericResponse('List not found.').not_found()
    else:
        response = GenericResponse('Missing list ID.').error()
    await pld.msg.channel.send(embed=response)
