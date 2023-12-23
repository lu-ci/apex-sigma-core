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


async def setcooldown(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    command = None
    cooldown = None
    if pld.args:
        if len(pld.args) == 2:
            command = pld.args[0].lower()
            if pld.args[1].isdigit():
                cooldown = int(pld.args[1])
        if command:
            if cooldown:
                if command in cmd.bot.modules.alts:
                    command = cmd.bot.modules.alts[command]
                if command in cmd.bot.modules.commands.keys():
                    cddata = {'command': command, 'cooldown': cooldown}
                    cddoc = await cmd.db.col.CommandCooldowns.find_one({'Command': command})
                    if not cddoc:
                        await cmd.db.col.CommandCooldowns.insert_one(cddata)
                    else:
                        await cmd.db.col.CommandCooldowns.update_one({'command': command}, {'$set': cddata})
                    response = GenericResponse(f'Command {command} now has a {cooldown}s cooldown.').ok()
                else:
                    response = GenericResponse(f'Command `{command}` not found.').not_found()
            else:
                response = GenericResponse('Missing or invalid cooldown.').error()
        else:
            response = GenericResponse('Missing command to edit.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
