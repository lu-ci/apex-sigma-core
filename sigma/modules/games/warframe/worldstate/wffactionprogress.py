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


async def wffactionprogress(_cmd: SigmaCommand, pld: CommandPayload):
    faction_projects = await WorldState().factionprojects
    if faction_projects:
        response = discord.Embed(color=0xff5050, title='Current Faction Progress')
        response.set_thumbnail(url=invasion_icon)
        for faction in faction_projects:
            response.add_field(name=faction['type'], value=f'{int(faction["progress"])}% Complete', inline=False)
    else:
        response = error('Could not retrieve Faction Projects data.')
    await pld.msg.channel.send(embed=response)
