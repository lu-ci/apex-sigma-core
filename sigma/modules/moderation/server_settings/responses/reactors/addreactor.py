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


async def addreactor(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if len(pld.args) >= 2:
            trigger = ' '.join(pld.args[:-1]).lower().strip()
            if len(trigger) <= 200:
                if '.' not in trigger:
                    reaction = pld.args[-1].strip('<> ')
                    auto_reactions = pld.settings.get('reactor_triggers', {})
                    res_text = 'updated' if trigger in auto_reactions else 'added'
                    auto_reactions.update({trigger: reaction})
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'reactor_triggers', auto_reactions)
                    response = GenericResponse(f'{trigger} has been {res_text}').ok()
                else:
                    response = GenericResponse('The trigger can\'t have a dot in it.').error()
            else:
                response = GenericResponse('The trigger has a limit of 200 characters.').error()
        else:
            response = GenericResponse('Invalid number of arguments.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
