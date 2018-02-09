# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


async def sell(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    currency = cmd.bot.cfg.pref.currency
    if args:
        inv = await cmd.db.get_inventory(message.author)
        if inv:
            lookup = ' '.join(args)
            if lookup == 'all':
                value = 0
                count = 0
                for invitem in inv:
                    item_ob_id = item_core.get_item_by_file_id(invitem['item_file_id'])
                    value += item_ob_id.value
                    count += 1
                    await cmd.db.del_from_inventory(message.author, invitem['item_id'])
                await cmd.db.add_currency(message.author, message.guild, value)
                currency = cmd.bot.cfg.pref.currency
                response = discord.Embed(color=0xc6e4b5, title=f'💶 You sold {count} items for {value} {currency}.')
            else:
                item_o = item_core.get_item_by_name(lookup)
                if item_o:
                    item = await cmd.db.get_inventory_item(message.author, item_o.file_id)
                else:
                    item = None
                if item:
                    value = item_o.value
                    await cmd.db.add_currency(message.author, message.guild, value)
                    await cmd.db.del_from_inventory(message.author, item['item_id'])
                    response = discord.Embed(color=0xc6e4b5,
                                             title=f'💶 You sold the {item_o.name} for {value} {currency}.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
