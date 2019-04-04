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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

nightwave_icon = 'https://i.imgur.com/nhivCTL.png'


def get_challenges(challenges: dict):
    """

    :param challenges:
    :type challenges:
    :return:
    :rtype:
    """
    dailies, weeklies, weeklies_hard = [], [], []
    for challenge in challenges:
        if challenge['xpAmount'] == '1000':
            dailies.append(challenge)
        if challenge['xpAmount'] == '3000':
            weeklies.append(challenge)
        if challenge['xpAmount'] == '5000':
            weeklies_hard.append(challenge)
    dailies_sorted = list(sorted(dailies, key=lambda x: x['description']))
    weeklies_sorted = list(sorted(weeklies, key=lambda x: x['description']))
    weeklies_hard_sorted = list(sorted(weeklies_hard, key=lambda x: x['description']))
    return dailies_sorted, weeklies_sorted, weeklies_hard_sorted


def get_offsets(challenges: list):
    """

    :param challenges:
    :type challenges:
    :return:
    :rtype:
    """
    offsets = []
    for challenge_list in challenges:
        expiry = arrow.get(challenge_list[0]['end']).timestamp
        offset = expiry - arrow.utcnow().timestamp
        offsets.append(str(datetime.timedelta(seconds=offset)))
    return offsets


def get_descriptions(challenges: list):
    """

    :param challenges:
    :type challenges:
    :return:
    :rtype:
    """
    descriptions = []
    for challenge_list in challenges:
        descriptions.append([c['description'] for c in challenge_list])
    return descriptions


async def wfnightwave(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    nw = await WorldState().nightwave
    if nw:
        response = discord.Embed(color=0x6b1724, title=f'Nightwave Season {nw["season"] + 1}', )
        response.set_thumbnail(url=nightwave_icon)
        dailies, weeklies, weeklies_hard = get_challenges(nw['challenges'])
        d_offset, w_offset, wh_offset = get_offsets([dailies, weeklies, weeklies_hard])
        d_descs, w_descs, wh_descs = get_descriptions([dailies, weeklies, weeklies_hard])
        response.add_field(name=f'Dailies - 1000rep - {d_offset}', value='\n'.join(d_descs), inline=False)
        response.add_field(name=f'Weeklies - 3000rep - {w_offset}', value='\n'.join(w_descs), inline=False)
        response.add_field(name=f'Weekly Elites - 5000rep - {wh_offset}', value='\n'.join(wh_descs), inline=False)
    else:
        response = error('Could not retrieve Nightwave data.')
    await pld.msg.channel.send(embed=response)
