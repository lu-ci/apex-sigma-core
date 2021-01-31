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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, not_found, warn
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.properties import cook_quality
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


async def cook(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    ongoing = Ongoing.is_ongoing('profession', pld.msg.author.id)
    if not ongoing:
        Ongoing.set_ongoing('profession', pld.msg.author.id)
        recipe_core = await get_recipe_core(cmd.db)
        item_core = await get_item_core(cmd.db)
        if pld.args:
            lookup = ' '.join(pld.args)
            recipe = recipe_core.find_recipe(lookup)
            used_items = []
            if recipe:
                req_satisfied = True
                for ingredient in recipe.ingredients:
                    user_inv = await cmd.db.get_inventory(pld.msg.author.id)
                    in_inventory = False
                    for item in user_inv:
                        if item['item_file_id'] == ingredient.file_id:
                            used_items.append(item)
                            in_inventory = True
                            break
                    if not in_inventory:
                        req_satisfied = False
                if req_satisfied:
                    cooked_item_data = item_core.get_item_by_name(recipe.name).generate_inventory_item()
                    await cmd.db.add_to_inventory(pld.msg.author.id, cooked_item_data)
                    await item_core.add_item_statistic(cmd.db, recipe, pld.msg.author)
                    for req_item in used_items:
                        if req_item.get('transferred'):
                            cooked_item_data.update({'transferred': True})
                        await cmd.db.del_from_inventory(pld.msg.author.id, req_item['item_id'])
                    quality = cook_quality[cooked_item_data['quality']]
                    connector = 'a'
                    if quality[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'an'
                    await cmd.db.add_resource(pld.msg.author.id, 'items', 1, cmd.name, pld.msg, True)
                    head_title = f'{recipe.icon} You made {connector} {quality.lower()} {recipe.name}'
                    response = discord.Embed(color=recipe.color, title=head_title)
                else:
                    response = error('You\'re missing ingredients.')
            else:
                response = not_found('Recipe not found.')
        else:
            response = error('Nothing inputted.')
        Ongoing.del_ongoing('profession', pld.msg.author.id)
    else:
        response = warn("Please wait while your previous item is done being prepared.")
    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
