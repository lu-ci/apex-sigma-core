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

from sigma.core.utilities.generic_responses import not_found, error
from sigma.modules.games.azur_lane.models.azur_lane_ship import AzurLaneShip, get_ship


async def azurlaneskills(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join(pld.args) if pld.args else None
    if lookup:
        ship = await get_ship(cmd.db, lookup)
        if ship:
            ship = AzurLaneShip(ship)
            skills = ship.skills.to_list()
            skill_lines = []
            for sindex, skill in enumerate(skills):
                skill_lines.append(f'**{sindex + 1}**: [{skill.type}] **{skill.name}** - {skill.description}')
            response = discord.Embed(color=ship.rarity_color)
            response.set_author(name=f'Azur Lane: {ship.name} Skills', icon_url=ship.images.small, url=ship.url)
            response.description = '\n'.join(skill_lines)
        else:
            response = not_found('Ship not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
