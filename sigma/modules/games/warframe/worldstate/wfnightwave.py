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

nightwave_icon = 'https://i.imgur.com/nhivCTL.png'


def get_xp_ammounts(challenges):
    """
    Gets a unique set of XP amounts from the given challenges.
    :param challenges: The challenges to parse.
    :type challenges: dict
    :return:
    :rtype: list[str]
    """
    xp_amounts = list(set([c['xpAmount'] for c in challenges]))
    xp_amounts.sort()
    return xp_amounts


def get_challenges(challenges, xp_amounts):
    """
    Sorts challenges based on how much rep they give.
    :param challenges: The challenges to be sorted.
    :type challenges: dict
    :param xp_amounts: The XP amounts for each difficulty.
    :type xp_amounts: list[str]
    :return:
    :rtype: (list, list, list)
    """
    dailies, weeklies, weeklies_hard = [], [], []
    for challenge in challenges:
        if challenge['xpAmount'] == xp_amounts[0]:
            dailies.append(challenge)
        if challenge['xpAmount'] == xp_amounts[1]:
            weeklies.append(challenge)
        if challenge['xpAmount'] == xp_amounts[2]:
            weeklies_hard.append(challenge)
    dailies_sorted = list(sorted(dailies, key=lambda x: x['description']))
    weeklies_sorted = list(sorted(weeklies, key=lambda x: x['description']))
    weeklies_hard_sorted = list(sorted(weeklies_hard, key=lambda x: x['description']))
    return dailies_sorted, weeklies_sorted, weeklies_hard_sorted


def get_offsets(challenges):
    """
    Gets the time offsets for challenge expiry in each category.
    :param challenges: The challenges to be parsed.
    :type challenges: list[list]
    :return:
    :rtype: list[str]
    """
    offsets = []
    for challenge_list in challenges:
        expiry = arrow.get(challenge_list[0]['end']).int_timestamp
        offset = expiry - arrow.utcnow().int_timestamp
        offsets.append(str(datetime.timedelta(seconds=offset)))
    return offsets


def get_descriptions(challenges):
    """
    Gets the description for challenges in each category.
    :param challenges: The challenges to be parsed.
    :type challenges: list[list]
    :return:
    :rtype: list[list]
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
        xp = get_xp_ammounts(nw['challenges'])
        dailies, weeklies, weeklies_hard = get_challenges(nw['challenges'], xp)
        d_offset, w_offset, wh_offset = get_offsets([dailies, weeklies, weeklies_hard])
        d_descs, w_descs, wh_descs = get_descriptions([dailies, weeklies, weeklies_hard])
        response.add_field(name=f'Dailies - {xp[0]}rep - {d_offset}', value='\n'.join(d_descs), inline=False)
        response.add_field(name=f'Weeklies - {xp[1]}rep - {w_offset}', value='\n'.join(w_descs), inline=False)
        response.add_field(name=f'Weekly Elites - {xp[2]}rep - {wh_offset}', value='\n'.join(wh_descs), inline=False)
    else:
        response = GenericResponse('Could not retrieve Nightwave data.').error()
    await pld.msg.channel.send(embed=response)
