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
from geopy.geocoders import Nominatim

from sigma.core.utilities.generic_responses import GenericResponse

map_icon = 'https://i.imgur.com/zFl9UPx.jpg'


async def mapsearch(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        search = ' '.join(pld.args)
        search_url = '+'.join(pld.args)
        geo_parser = Nominatim(user_agent=cmd.bot.get_agent(True))
        location = geo_parser.geocode(search)
        if location:
            lat = location.latitude
            lon = location.longitude
            maps_url = f'https://www.google.rs/maps/search/{search_url}/@{lat},{lon},11z?hl=en'
            response = discord.Embed(color=0xdd4e40)
            response.set_author(name=f'{location}', icon_url=map_icon, url=maps_url)
        else:
            maps_url = f'https://www.google.rs/maps/search/{search_url}'
            response = discord.Embed(color=0xdd4e40)
            response.set_author(name=f'Broad Search: {search.title()}', icon_url=map_icon, url=maps_url)
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
