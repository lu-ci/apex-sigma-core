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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar, paginate
from .nodes.item_core import ItemCore

item_core = None


async def itemstatistics(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    all_stats = await cmd.db[cmd.db.db_cfg.database].ItemStatistics.find_one({'UserID': target.id}) or {}
    if '_id' in all_stats:
        all_stats.pop('_id')
        all_stats.pop('UserID')
    all_stats = [[x, all_stats.get(x)] for x in all_stats.keys()]
    mem_count = len(all_stats)
    all_stats = sorted(all_stats, key=lambda k: k[1], reverse=True)
    page = args[0] if args else 1
    all_stats, page = paginate(all_stats, page)
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
    await message.channel.send(embed=response)
