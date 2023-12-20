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

from sigma.core.utilities.generic_responses import GenericResponse


async def listsettings(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.args) > 1:
        mode = None
        valid_mode = True
        mode_name = pld.args[1].lower()
        if mode_name == 'private':
            mode = 'private'
        elif mode_name == 'locked':
            mode = 'locked'
        elif mode_name == 'public':
            mode = None
        else:
            valid_mode = False
        if valid_mode:
            lookup_data = {'server_id': pld.msg.guild.id, 'list_id': pld.args[0].lower()}
            list_coll = cmd.db[cmd.db.db_name].CustomLists
            list_file = await list_coll.find_one(lookup_data)
            if list_file:
                list_id = list_file.get('list_id')
                if list_file.get('user_id') == pld.msg.author.id:
                    list_file.update({'mode': mode})
                    await list_coll.update_one(lookup_data, {'$set': list_file})
                    response = GenericResponse(f'List `{list_id}` marked as {mode or "public"}.').ok()
                else:
                    response = GenericResponse('You didn\'t make this list.').denied()
            else:
                response = GenericResponse('Invalid list ID.').error()
        else:
            response = GenericResponse('Invalid mode.').error()
    else:
        response = GenericResponse('Not enough arguments.').error()
    await pld.msg.channel.send(embed=response)
