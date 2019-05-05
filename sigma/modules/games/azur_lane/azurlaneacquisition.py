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

import discord

from sigma.core.utilities.generic_responses import not_found, error
from sigma.modules.games.azur_lane.models.azur_lane_ship import get_ship, AzurLaneShip


async def azurlaneacquisition(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join([pla for pla in pld.args if not pla.startswith('--')])
    try:
        lookup = int(lookup)
    except ValueError:
        pass
    if lookup:
        ship = await get_ship(cmd.db, lookup)
        if ship:
            ship = AzurLaneShip(ship)
            response = discord.Embed(color=ship.rarity_color)
            response.set_author(name=f'Azur Lane: {ship.name} Acquisition', icon_url=ship.images.small, url=ship.url)
            if ship.acquisition.notes:
                response.description = ship.acquisition.notes
            if ship.acquisition.construction.possible:
                cstr_time = datetime.timedelta(seconds=ship.acquisition.construction.time)
                cstr_status = f'Construction is possible and takes {cstr_time}.'
            else:
                cstr_status = 'Construction not possible.'
            cstr_types = []
            for const_type_key in ['light', 'heavy', 'special', 'limited', 'exchange']:
                const_possible = getattr(ship.acquisition.construction, const_type_key)
                cstr_types.append(f"{const_type_key.title()}: {'✅' if const_possible else '❌'}")
            cstr_block = f'{cstr_status}\n{" | ".join(cstr_types)}'
            response.add_field(name='Construction', value=cstr_block, inline=False)
            possible_missions = []
            possible_missions_cache = {}
            for mission in ship.acquisition.missions:
                if mission.possible:
                    nodes = possible_missions_cache.get(mission.chapter, [])
                    mission_name = f'**{mission.map}**' if mission.boss_only else str(mission.map)
                    if mission_name not in nodes:
                        nodes.append(mission_name)
                        possible_missions_cache.update({mission.chapter: nodes})
            for pm_key in possible_missions_cache:
                possible_missions.append(f'Chapter {pm_key}: Nodes {", ".join(possible_missions_cache.get(pm_key))}')
            if len(possible_missions) == 0:
                smsn_block = 'Acquisition from sortie battles not possible.'
            else:
                smsn_block = '\n'.join(possible_missions)
                response.set_footer(text='Bolded nodes indicate that only the boss drops this ship.')
            response.add_field(name='Mission Drop', value=smsn_block, inline=False)
        else:
            response = not_found('Ship not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
