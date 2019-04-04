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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

invasion_icon = 'https://i.imgur.com/QUPS0ql.png'


async def wfinvasions(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    invasions = await WorldState().invasions
    if invasions:
        response = discord.Embed(color=0xff5050, title='Currently Ongoing Invasions')
        response.set_thumbnail(url=invasion_icon)
        for invasion in invasions:
            active = invasion['endScore'] > abs(invasion['score'])
            if active:
                percent = round((abs(invasion['score']) / invasion['endScore']) * 100, 2)
                invasion_desc = f'Location: {invasion["location"]}'
                reward_def = invasion['rewardsDefender']['items'][0]
                reward_one = f'{reward_def["count"]} {reward_def["name"]}'
                invasion_desc += f'\nRewards: {reward_one}'
                if invasion.get('rewardsAttacker'):
                    reward_atk = invasion['rewardsAttacker']['items'][0]
                    reward_two = f'{reward_atk["count"]} {reward_atk["name"]}'
                    invasion_desc += f' vs {reward_two}'
                invasion_title = f'{invasion["factionDefender"]} vs {invasion["factionAttacker"]} - {percent}%'
                response.add_field(name=invasion_title, value=f'{invasion_desc}', inline=False)
    else:
        response = error('Could not retrieve Invasion data.')
    await pld.msg.channel.send(embed=response)
