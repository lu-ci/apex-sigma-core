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


async def roleid(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    embed = True
    if pld.args:
        lookup = ' '.join(pld.args)
        if pld.args[-1].lower() == '--text':
            embed = False
            lookup = ' '.join(pld.args[:-1])
        role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), pld.msg.guild.roles)
        if role:
            if embed:
                response = discord.Embed(color=0x3B88C3)
                response.add_field(name=f'ℹ️ {role.name}', value=f'`{role.id}`')
            else:
                response = role.id
        else:
            embed = True
            response = GenericResponse(f'{lookup} not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    if embed:
        await pld.msg.channel.send(embed=response)
    else:
        await pld.msg.channel.send(response)
