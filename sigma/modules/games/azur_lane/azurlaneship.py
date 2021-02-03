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


async def azurlaneship(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join([pla for pla in pld.args if not pla.startswith('--')])
    no_image = '--no-image' in pld.args
    retrofit = '--retrofit' in pld.args
    awoken = '--awaken' in pld.args
    try:
        lookup = int(lookup)
    except ValueError:
        pass
    if lookup:
        ship = await get_ship(cmd.db, lookup)
        if ship:
            ship = AzurLaneShip(ship)
            response = discord.Embed(color=ship.rarity_color)
            response.set_author(name=f'Azur Lane: {ship.name}', icon_url=ship.images.small, url=ship.url)
            if not no_image:
                response.set_image(url=ship.images.main.url)
            for quote in ship.quotes:
                desc_quotes = ['self introduction', 'acquisition']
                if quote.event.lower() in desc_quotes and quote.en:
                    response.description = quote.en
                    break
            if ship.images.chibi:
                response.set_thumbnail(url=ship.images.chibi)
            if retrofit:
                response.add_field(name='Retrofit', value=f'```py\n{ship.stats.retrofit.describe(awoken)}\n```')
            else:
                response.add_field(name='Statistics', value=f'```py\n{ship.stats.normal.describe(awoken)}\n```')
            if ship.faction_short:
                footer_text = f'{ship.faction_short} {ship.name} of the {ship.faction}.'
            else:
                footer_text = f'{ship.name} of the {ship.faction}.'
            response.set_footer(text=footer_text, icon_url=ship.faction_icon or discord.Embed.Empty)
        else:
            response = GenericResponse('Ship not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
