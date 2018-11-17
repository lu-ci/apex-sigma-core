# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def destroyitem(cmd: SigmaCommand, pld: CommandPayload):
    item_core = await get_item_core(cmd.db)
    if pld.args:
        id_lookup = pld.args[0]
        inv_item = await cmd.db[cmd.db.db_nam].Inventory.find_one({'items.item_id': id_lookup})
        if inv_item:
            target = await cmd.bot.get_user(inv_item.get('user_id'))
            item_data = None
            for item in inv_item.get('items', []):
                if item.get('item_id') == id_lookup:
                    item_data = item
                    break
            item_id = item_data.get('item_id')
            item_file_id = item_data.get('item_file_id')
            await cmd.db.del_from_inventory(target, item_id)
            item_o = item_core.get_item_by_file_id(item_file_id)
            connector = 'a'
            if item_o.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            success_text = f'{item_o.icon} I have removed {connector} {item_o.name} from {target.display_name}.'
            response = discord.Embed(color=item_o.color, title=success_text)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No item with that ID was found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
