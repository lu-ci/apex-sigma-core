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


async def starboardlimit(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        starboard_doc = pld.settings.get('starboard') or {}
        if pld.args:
            try:
                new_limit = abs(int(pld.args[0]))
            except ValueError:
                new_limit = None
            if new_limit is not None:
                starboard_doc.update({'limit': int(new_limit)})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'starboard', starboard_doc)
                response = GenericResponse(f'Starboard limit set to {new_limit}.').ok()
            else:
                response = GenericResponse('Limit must be a number.').error()
        else:
            limit = starboard_doc.get('limit')
            if limit:
                response = discord.Embed(color=0xFFAC33, title=f'🌟 The current limit is {limit}')
            else:
                response = GenericResponse('A limit has not been set.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
