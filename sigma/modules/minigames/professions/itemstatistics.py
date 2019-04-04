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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def itemstatistics(cmd: SigmaCommand, pld: CommandPayload):
    item_core = await get_item_core(cmd.db)
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
    else:
        target = pld.msg.author
    all_stats = await cmd.db[cmd.db.db_nam].ItemStatistics.find_one({'user_id': target.id}) or {}
    if '_id' in all_stats:
        all_stats.pop('_id')
        all_stats.pop('user_id')
    all_stats = [[x, all_stats.get(x)] for x in all_stats.keys()]
    mem_count = len(all_stats)
    all_stats = sorted(all_stats, key=lambda k: k[1], reverse=True)
    page = pld.args[0] if pld.args else 1
    all_stats, page = PaginatorCore.paginate(all_stats, page)
    total_count = len([i for i in item_core.all_items if i.rarity != 0])
    listing = []
    for stat in all_stats:
        item_o = item_core.get_item_by_file_id(stat[0])
        if item_o.rarity != 0:
            amount = stat[1]
            listing.append([item_o.name, amount])
    out_table = boop(listing, ['Item', 'Count'])
    response = discord.Embed(color=0xc16a4f)
    response.set_author(name=f'{target.name}\'s Item Statistics', icon_url=user_avatar(target))
    response.description = f'```hs\n{out_table}\n```'
    response.set_footer(text=f'[Page {page}] {target.name} has found {mem_count} out of {total_count} items.')
    await pld.msg.channel.send(embed=response)
