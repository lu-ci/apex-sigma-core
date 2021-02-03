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


async def renamecommand(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            if len(pld.args) == 2:
                old_trigger = pld.args[0].lower()
                new_trigger = pld.args[1].lower()
                if '.' not in new_trigger:
                    if new_trigger not in cmd.bot.modules.commands and new_trigger not in cmd.bot.modules.alts:
                        custom_commands = pld.settings.get('custom_commands') or {}
                        if old_trigger in custom_commands:
                            if new_trigger not in custom_commands:
                                custom_commands.update({new_trigger: custom_commands[old_trigger]})
                                del custom_commands[old_trigger]
                                await cmd.db.set_guild_settings(pld.msg.guild.id, 'custom_commands', custom_commands)
                                response = GenericResponse(f'{old_trigger} updated.').ok()
                            else:
                                response = GenericResponse('The new trigger is already a command.').error()
                        else:
                            response = GenericResponse('Command not found.').not_found()
                    else:
                        response = GenericResponse('Can\'t replace an existing core command.').error()
                else:
                    response = GenericResponse('The command can\'t have a dot in it.').error()
            else:
                response = GenericResponse('Invalid number of arguments.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
