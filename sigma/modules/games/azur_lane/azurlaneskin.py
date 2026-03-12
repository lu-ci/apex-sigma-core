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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.games.azur_lane.models.azur_lane_ship import AzurLaneShip, get_ship


async def azurlaneskin(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    qry = ' '.join(pld.args) if pld.args else ''
    if qry and ';' in qry:
        ship_qry, skin_qry = [qix.strip() for qix in qry.split(';')[:2]]
        ship = await get_ship(cmd.db, ship_qry)
        if ship:
            ship = AzurLaneShip(ship)
            skin = ship.images.get_skin(skin_qry)
            if skin:
                skin_url = f'{ship.url}#{skin.name.replace(" ", "%20")}'
                title = f'{ship.name}: {skin.name}'
                response = discord.Embed(color=ship.rarity_color)
                response.set_author(name=title, icon_url=ship.images.small, url=skin_url)
                response.set_image(url=skin.url)
            else:
                response = GenericResponse(f'Couldn\'t find that skin for {ship.name}.').not_found()
        else:
            response = GenericResponse('Ship not found.').not_found()
    else:
        response = GenericResponse('Invalid input. Please follow the usage example.').error()
    await pld.msg.channel.send(embed=response)
