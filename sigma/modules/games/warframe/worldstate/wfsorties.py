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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.games.warframe.commons.worldstate import WorldState

sortie_icon = 'https://i.imgur.com/Okg20Uk.png'


async def wfsorties(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    sorties = await WorldState().sorties
    if sorties:
        expiry_dt = arrow.get(sorties['end']).datetime
        response = discord.Embed(color=0x6666FF, title='Current Sorties', timestamp=expiry_dt)
        response.set_thumbnail(url=sortie_icon)
        for i, sortie in enumerate(sorties['missions']):
            sortie_desc = f'Type: {sortie["missionType"]}'
            sortie_desc += f'\nLocation: {sortie["location"]}'
            sortie_desc += f'\nModifier: {sortie["modifier"]}'
            response.add_field(name=f'Mission {i + 1}', value=sortie_desc, inline=False)
        offset = sorties['end'] - arrow.utcnow().int_timestamp
        expiry = str(datetime.timedelta(seconds=offset))
        response.set_footer(text=f'Resets in {expiry}')
    else:
        response = GenericResponse('Could not retrieve Sorties data.').error()
    await pld.msg.channel.send(embed=response)
