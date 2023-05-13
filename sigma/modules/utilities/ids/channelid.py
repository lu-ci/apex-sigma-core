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


async def channelid(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    embed = True
    if pld.args:
        if pld.args[-1].lower() == '--text':
            embed = False
    if pld.msg.channel_mentions:
        target = pld.msg.channel_mentions[0]
    else:
        target = pld.msg.channel
    response = discord.Embed(color=0x3B88C3)
    response.add_field(name=f'ℹ️ {target.name}', value=f'`{target.id}`')
    if embed:
        await pld.msg.channel.send(embed=response)
    else:
        await pld.msg.channel.send(f'{target.id}')
