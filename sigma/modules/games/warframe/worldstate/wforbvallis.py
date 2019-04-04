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

import datetime

import arrow
import discord

from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

fissure_icon = 'https://i.imgur.com/vANGxqe.png'
temps = {'warm': {'color': 0xFFCC4D, 'icon': '🔥'}, 'cold': {'color': 0x88C9F9, 'icon': '❄'}}


async def wforbvallis(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    time = await WorldState().vallistime
    if time:
        temp, temp_in = ('warm', 'Cold') if time['isWarm'] else ('cold', 'Warm')
        color, icon = temps[temp].values()
        offset = arrow.get(time['expiry']).timestamp - arrow.utcnow().timestamp
        in_time = str(datetime.timedelta(seconds=offset)).partition(':')[2]
        text_desc = f'Next {temp_in} Cycle: **{in_time}**'
        response = discord.Embed(color=color)
        response.add_field(name=f'{icon} It\'s Currently {temp.title()}', value=text_desc)
    else:
        response = error('Could not retrieve Orb Vallis data.')
    await pld.msg.channel.send(embed=response)
