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

bonus = {
    'cat': 'https://httpcats.com',
    'dog': 'https://http.dog',
    'goat': 'https://httpgoats.com',
    'garden': 'https://http.garden'
}


async def httpstatus(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = pld.args[0] if pld.args else None
    if lookup:
        status_data = await cmd.db[cmd.db.db_name].HTTPStatusData.find_one({'code': lookup})
        if status_data:
            response = discord.Embed(color=0x3B88C3)
            status_id = status_data.get('code')
            for status in status_data.get('messages'):
                message = status.get('message')
                if status.get('expanded'):
                    message += f' ({status.get("provider")})'
                response.add_field(name=f'🌐 {status_id}: {message}', value=status.get('description'), inline=False)
            bonus_arg = pld.args[-1].lower()
            if bonus_arg in bonus.keys() and lookup.isdigit():
                response.set_image(url=f'{bonus.get(bonus_arg)}/{lookup}.jpg')
        else:
            response = GenericResponse('Response code not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
