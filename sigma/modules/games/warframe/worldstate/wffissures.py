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

fissure_icon = 'https://i.imgur.com/vANGxqe.png'


def sort_fissures(fissures):
    """
    :type fissures: list[dict]
    :rtype: list[dict]
    """
    lith, meso, neo, axi, requiem = [], [], [], [], []
    for fissure in fissures:
        if fissure['tier'] == 'Lith':
            lith.append(fissure)
        if fissure['tier'] == 'Meso':
            meso.append(fissure)
        if fissure['tier'] == 'Neo':
            neo.append(fissure)
        if fissure['tier'] == 'Axi':
            axi.append(fissure)
        if fissure['tier'] == 'Requiem':
            requiem.append(fissure)
    return lith + meso + neo + axi + requiem


async def wffissures(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    fissures = await WorldState().fissures
    if fissures:
        response = discord.Embed(color=0x66ccff, title='Currently Ongoing Fissures')
        void_storms = []
        for fissure in sort_fissures(fissures):
            fissure_desc = f'Location: {fissure["nodeKey"]} - {fissure["missionType"]}'
            fissure_desc += f'\nFaction: {fissure["enemy"]}'
            offset = arrow.get(fissure['expiry']).int_timestamp - arrow.utcnow().int_timestamp
            expiry = str(datetime.timedelta(seconds=offset))
            fissure_desc += f'\nDisappears In: {expiry}'
            name = f'{fissure["tier"]} Void Fissure'
            if fissure['isStorm']:
                name += ' (Void Storm)'
                void_storms.append((name, fissure_desc))
            else:
                response.add_field(name=name, value=fissure_desc, inline=False)
        for name, desc in void_storms:
            response.add_field(name=name, value=desc, inline=False)
        response.set_footer(text='Timers are not updated live.')
        response.set_thumbnail(url=fissure_icon)
    else:
        response = GenericResponse('Could not retrieve Fissure data.').error()
    await pld.msg.channel.send(embed=response)
