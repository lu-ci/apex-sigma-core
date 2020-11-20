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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


async def inspect(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    recipe_core = await get_recipe_core(cmd.db)
    item_core = await get_item_core(cmd.db)
    if pld.args:
        lookup = ' '.join(pld.args)
        item = item_core.get_item_by_name(lookup)
        if item:
            if item.rarity != 0:
                stat_coll = cmd.db[cmd.db.db_nam].ItemStatistics
                all_stats = await stat_coll.find_one({'user_id': pld.msg.author.id}) or {}
                item_total = 0
                all_stat_docs = await stat_coll.find({item.file_id: {'$exists': True}}).to_list(None)
                for stat_doc in all_stat_docs:
                    item_total += stat_doc.get(item.file_id) or 0
                stat_count = all_stats.get(item.file_id) or 0
                owned_item = await cmd.db.get_inventory_item(pld.msg.author.id, item.file_id)
                response = item.make_inspect_embed(cmd.bot.cfg.pref.currency, recipe_core)
                footer = f'You Found: {stat_count} | Total Found: {item_total}'
                if item.rarity == 11:
                    pfx = cmd.db.get_prefix(pld.settings)
                    footer += f' | Try {pfx}recipe {item.name}'
                if owned_item:
                    inv = await cmd.db.get_inventory(pld.msg.author.id)
                    count = len([i for i in inv if i.get('item_file_id') == item.file_id])
                    footer += f' | Owned: {count} | ID: {owned_item.get("item_id")}'
                    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
                response.set_footer(text=footer)
            else:
                response = error('Sorry but that\'s trash.')
        else:
            response = not_found('Item not found.')
    else:
        response = error('Nothing inputted.')
        response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
