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


def sort_fissures(fissures):
    """
    :param fissures:
    :type fissures: list[dict]
    :return:
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
        for fissure in sort_fissures(fissures):
            fissure_desc = f'Location: {fissure["location"]} - {fissure["missionType"]}'
            fissure_desc += f'\nFaction: {fissure["faction"]}'
            offset = fissure['end'] - arrow.utcnow().int_timestamp
            expiry = str(datetime.timedelta(seconds=offset))
            fissure_desc += f'\nDisappears In: {expiry}'
            response.add_field(name=f'{fissure["tier"]} Void Fissure', value=fissure_desc, inline=False)
        response.set_footer(text='Timers are not updated live.')
        response.set_thumbnail(url=fissure_icon)
    else:
        response = error('Could not retrieve Fissure data.')
    await pld.msg.channel.send(embed=response)
