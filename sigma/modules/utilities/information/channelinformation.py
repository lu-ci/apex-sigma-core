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

import arrow
import discord


async def channelinformation(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    chan = pld.msg.channel_mentions[0] if pld.msg.channel_mentions else pld.msg.channel
    response = discord.Embed(color=0x1B6F5F)
    creation_time = arrow.get(chan.created_at).format('DD. MMMM YYYY')
    info_text = f'Name: **{chan.name}**'
    info_text += f'\nID: **{chan.id}**'
    info_text += f'\nPosition: **{chan.position}**'
    info_text += f'\nNSFW: **{chan.nsfw}**'
    info_text += f'\nCreated: **{creation_time}**'
    response.add_field(name=f'#{chan.name} Information', value=info_text)
    await pld.msg.channel.send(embed=response)
