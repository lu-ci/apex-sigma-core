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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.inventory import get_page_number, get_filter, is_ingredient
from sigma.modules.minigames.professions.market.market_expiration import check_expiry
from sigma.modules.minigames.professions.market.market_models import MarketEntry
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


async def marketlist(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    ic = await get_item_core(cmd.db)
    reci_core = await get_recipe_core(cmd.db)
    await check_expiry(cmd.db)
    lookup = get_filter(pld.args)
    entries = []
    title = None
    if lookup:
        item = ic.get_item_by_name(lookup)
        if item:
            title = f'Cheapest {item.rarity_name} {item.name} listings.'
            sort = ('price', -1)
            entries = await MarketEntry.find_all_items(cmd.db, item.file_id, sort=sort)
    else:
        title = 'Most recent listings.'
        sort = ('stamp', -1)
        entries = await MarketEntry.find_all(cmd.db, sort=sort)
    if entries:
        total_count = len(entries)
        entries, page = PaginatorCore.paginate(entries, get_page_number(pld.args))
        start_range, end_range = (page - 1) * 10, page * 10
        headers = ['Type', 'Name', 'Price', 'Rarity']
        to_format = []
        for entry in entries:
            item = ic.get_item_by_file_id(entry.item)
            in_rec = '*' if is_ingredient(reci_core.recipes, item) else ''
            to_format.append(
                [
                    item.type,
                    f'{item.name}{in_rec}',
                    f'{entry.price}',
                    f'{item.rarity_name.title()}'
                ]
            )
        output = boop(to_format, column_names=headers)
        response = discord.Embed(color=0x4289c1)
        inv_text = f'Showing items {start_range}-{end_range}.'
        inv_text += f'\nThere are {total_count} items on the open market.'
        response.add_field(name=f'💶 {title}', value=f'```py\n{inv_text}\n```')
        response.add_field(name=f'📋 Items Currently On Page {page}', value=f'```hs\n{output}\n```', inline=False)
    else:
        response = GenericResponse('I couldn\'t find anything with that name.').error()
    await pld.msg.channel.send(embed=response)
