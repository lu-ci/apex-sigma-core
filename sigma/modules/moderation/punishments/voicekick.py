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

from sigma.core.utilities.data_processing import get_broad_target
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.permission_processing import hierarchy_permit


async def voicekick(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).kick_members:
        target = get_broad_target(pld)
        if target:
            if cmd.bot.user.id != target.id:
                if pld.msg.author.id != target.id:
                    above_hier = hierarchy_permit(pld.msg.author, target)
                    is_admin = pld.msg.channel.permissions_for(pld.msg.author).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(pld.msg.guild.me, target)
                        if above_me:
                            if target.voice:
                                tvc = target.voice.channel
                                tempvc = discord.utils.find(lambda x: x.name == 'Kick Hall', pld.msg.guild.channels)
                                if not tempvc:
                                    tempvc = await pld.msg.guild.create_voice_channel('Kick Hall')
                                await target.move_to(tempvc)
                                await tempvc.delete()
                                remove_title = f'👢 {target.name} has been removed from {tvc.name}.'
                                response = discord.Embed(color=0xc1694f, title=remove_title)
                            else:
                                response = GenericResponse(f'{target.name} is not in a voice channel.').error()
                        else:
                            response = GenericResponse('Target is above my highest role.').denied()
                    else:
                        response = GenericResponse('Can\'t kick someone equal or above you.').denied()
                else:
                    response = GenericResponse('You can\'t kick yourself.').error()
            else:
                response = GenericResponse('I can\'t kick myself.').error()
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Kick permissions needed.').denied()
    await pld.msg.channel.send(embed=response)
