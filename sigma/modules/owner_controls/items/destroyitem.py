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
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def destroyitem(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item_core = await get_item_core(cmd.db)
    if pld.args:
        id_lookup = pld.args[0]
        inv_item = await cmd.db[cmd.db.db_name].Inventory.find_one({'items.item_id': id_lookup})
        if inv_item:
            target_id = inv_item.get('user_id')
            target = await cmd.bot.get_user(target_id)
            item_data = None
            for item in inv_item.get('items', []):
                if item.get('item_id') == id_lookup:
                    item_data = item
                    break
            item_id = item_data.get('item_id')
            item_file_id = item_data.get('item_file_id')
            await cmd.db.del_from_inventory(target_id, item_id)
            item_o = item_core.get_item_by_file_id(item_file_id)
            connector = 'a'
            if item_o.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            target_name = target.display_name if target else 'Unknown User'
            success_text = f'{item_o.icon} I have removed {connector} {item_o.name} from {target_name}.'
            response = discord.Embed(color=item_o.color, title=success_text)
        else:
            response = GenericResponse('No item with that ID was found.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
