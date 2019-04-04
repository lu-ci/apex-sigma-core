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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

darvo_icon = 'https://i.imgur.com/bpDzO9W.png'


async def wfdailydeal(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item = await WorldState().dailydeals
    if item:
        end_time = arrow.get(item['end']).humanize()
        item_out = f"**Item:** {item['item']['name']}\n"
        item_out += f'**Sale Price:** {item["price"]} Plat\n'
        item_out += f'**Original Price:** {item["originalPrice"]} Plat\n'
        discount = int((1 - item['price'] / item['originalPrice']) * 100)
        item_out += f"**Discount:** {discount}%\n"
        item_out += f'**Quantity:** {item["stock"] - item["sold"]}/{item["stock"]}'
        response = discord.Embed(color=0xff6100)
        response.add_field(name="Darvo's Daily Deal", value=item_out)
        response.set_footer(text=f'Sale ends {end_time}', icon_url=darvo_icon)
    else:
        response = error('Could not retrieve Daily Deal data.')
    await pld.msg.channel.send(embed=response)
