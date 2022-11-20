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


async def autoroletimeout(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if pld.args:
            try:
                timeout = abs(int(pld.args[0]))
            except ValueError:
                timeout = None
            if timeout is not None:
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'auto_role_timeout', timeout)
                response = GenericResponse(f'Timeout set to {timeout} seconds.').ok()
            else:
                response = GenericResponse('This role is above my highest role.').error()
        else:
            timeout = pld.settings.get('auto_role_timeout', 0)
            response = discord.Embed(color=0x696969, title=f'🕙 The current timeout is {timeout} seconds.')
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
