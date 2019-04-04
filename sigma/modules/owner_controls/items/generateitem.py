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
from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def generateitem(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item_core = await get_item_core(cmd.db)
    if pld.args:
        if pld.msg.mentions:
            if len(pld.args) >= 2:
                target = pld.msg.mentions[0]
                lookup = ' '.join(pld.args[1:])
                item = item_core.get_item_by_name(lookup)
                if item:
                    connector = 'a'
                    if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'an'
                    data_for_inv = item.generate_inventory_item()
                    await cmd.db.add_to_inventory(target.id, data_for_inv)
                    success_text = f'{item.icon} I have given {connector} {item.name} to {target.display_name}.'
                    response = discord.Embed(color=item.color, title=success_text)
                else:
                    response = not_found(f'{lookup} not found.')
            else:
                response = error('Not enough arguments.')
        else:
            response = error('No user targeted.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
