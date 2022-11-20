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


async def suggestionchannel(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if pld.msg.channel_mentions:
            target = pld.msg.channel_mentions[0]
        else:
            if pld.args:
                if pld.args[0].lower() == 'disable':
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'suggestion_channel', None)
                    response = GenericResponse('Suggestion Channel disabled.').ok()
                    await pld.msg.channel.send(embed=response)
                return
            else:
                target = pld.msg.channel
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'suggestion_channel', target.id)
        response = GenericResponse(f'Suggestion Channel set to #{target.name}.').ok()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
