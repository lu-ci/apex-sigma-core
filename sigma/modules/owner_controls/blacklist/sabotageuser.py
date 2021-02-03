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


async def sabotageuser(cmd, pld):
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
            if target_id not in cmd.bot.cfg.dsc.owners:
                target = await cmd.bot.get_user(target_id)
                if target:
                    target_id = target.id
                    target_name = target.name
                else:
                    target_name = target_id
                sabotage_file = await cmd.db.is_sabotaged(target_id)
                if sabotage_file:
                    icon, result, status = '🔓', 'unsabotaged', False
                else:
                    icon, result, status = '🔒', 'sabotaged', True
                await cmd.db.set_profile(target_id, 'sabotaged', status)
                response = discord.Embed(color=0xFFCC4D, title=f'{icon} {target_name} has been {result}.')
            else:
                response = GenericResponse('That target is immune.').error()
        else:
            response = GenericResponse('Invalid user ID.').error()
    else:
        response = GenericResponse('Missing user ID.').error()
    await pld.msg.channel.send(embed=response)
