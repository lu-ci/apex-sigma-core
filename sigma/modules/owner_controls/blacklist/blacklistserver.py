﻿"""
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


async def blacklistserver(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            target_id = abs(int(pld.args[0]))
        except ValueError:
            target_id = None
        if target_id:
            target = await cmd.bot.get_guild(target_id)
            if target:
                target_id = target.id
                target_name = target.name
            else:
                target_name = target_id
            black_file = await cmd.db.col.BlacklistedServers.find_one({'server_id': target_id})
            if black_file:
                await cmd.db.col.BlacklistedServers.delete_one({'server_id': target_id})
                icon, result = '🔓', 'un-blacklisted'
            else:
                await cmd.db.col.BlacklistedServers.insert_one({'server_id': target_id})
                icon, result = '🔒', 'blacklisted'
            response = discord.Embed(color=0xFFCC4D, title=f'{icon} {target_name} has been {result}.')
            await cmd.db.cache.del_cache(target_id)
            await cmd.db.cache.del_cache(f'{target_id}_checked')
        else:
            response = GenericResponse('Invalid guild ID.').error()
    else:
        response = GenericResponse('Missing guild ID.').error()
    await pld.msg.channel.send(embed=response)
