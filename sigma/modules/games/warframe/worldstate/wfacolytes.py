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
from humanfriendly.tables import format_pretty_table

from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

stalker_icon = 'https://vignette.wikia.nocookie.net/warframe/images/0/06/9PxL9MAPh4.png'


async def wfacolytes(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    acolytes = await WorldState().acolytes
    if acolytes:
        data_list = []
        headers = ['Name', 'Health', 'Location']
        for acolyte in acolytes:
            name = acolyte.get('name')
            health = f"{round(acolyte.get('health') * 100, 2)}%"
            if acolyte.get('discovered'):
                location = acolyte.get('location')
            else:
                location = 'Unknown'
            entry = [name, health, location]
            data_list.append(entry)
        data_table = format_pretty_table(data_list, headers)
        response = discord.Embed(color=0xcc0000)
        response.set_author(name='Warframe Acolytes Data', icon_url=stalker_icon)
        response.description = f'```hs\n{data_table}\n```'
    else:
        response = error('No data on the Acolytes.')
    await pld.msg.channel.send(embed=response)
