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
from .nodes.item_core import ItemCore

item_core = None


async def sell_item_ids(db, user, items):
    inv = await db.get_inventory(user)
    for item in items:
        for inv_item in inv:
            if inv_item['item_id'] == item:
                inv.remove(inv_item)
    await db.update_inv(user, inv)


async def filtersell(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        full_qry = ' '.join(args)
        arguments = full_qry.split(':')
        if len(arguments) >= 2:
            mode = arguments[0].lower()
            lookup = ' '.join(arguments[1:])
            inv = await cmd.db.get_inventory(message.author)
            if inv:
                value = 0
                count = 0
                if mode == 'name':
                    attribute = 'name'
                elif mode == 'type':
                    attribute = 'type'
                elif mode == 'rarity' or mode == 'quality':
                    attribute = 'rarity_name'
                else:
                    attribute = None
                if attribute:
                    sell_id_list = []
                    for item in inv:
                        item_ob_id = item_core.get_item_by_file_id(item['item_file_id'])
                        item_attribute = getattr(item_ob_id, attribute)
                        if item_attribute.lower() == lookup.lower():
                            value += item_ob_id.value
                            count += 1
                            sell_id_list.append(item['item_id'])
                    await sell_item_ids(cmd.db, message.author, sell_id_list)
                    await cmd.db.add_currency(message.author, message.guild, value)
                    currency = cmd.bot.cfg.pref.currency
                    ender = 's' if count != 1 else ''
                    response = discord.Embed(color=0xc6e4b5)
                    response.title = f'💶 You sold {count} item{ender} for {value} {currency}.'
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid arguments.')
            else:
                response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty...')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
