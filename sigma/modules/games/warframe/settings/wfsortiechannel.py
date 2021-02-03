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


async def wfsortiechannel(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_channels:
        if pld.msg.channel_mentions:
            target_channel = pld.msg.channel_mentions[0]
        else:
            if pld.args:
                if pld.args[0].lower() == 'disable':
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'warframe_sortie_channel', None)
                    response = GenericResponse('Warframe Sortie Channel disabled.').ok()
                    await pld.msg.channel.send(embed=response)
                return
            else:
                target_channel = pld.msg.channel
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'warframe_sortie_channel', target_channel.id)
        response = GenericResponse(f'Warframe Sortie Channel set to #{target_channel.name}').ok()
    else:
        response = GenericResponse('Access Denied. Manage Channels needed.').denied()
    await pld.msg.channel.send(embed=response)
