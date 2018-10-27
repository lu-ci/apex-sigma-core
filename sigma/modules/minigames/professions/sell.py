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
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def sell(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    item_core = await get_item_core(cmd.db)
    currency = cmd.bot.cfg.pref.currency
    if args:
        inv = await cmd.db.get_inventory(message.author.id)
        if inv:
            lookup = ' '.join(args)
            if lookup.lower() == 'all':
                value = 0
                count = 0
                for invitem in inv.copy():
                    item_ob_id = item_core.get_item_by_file_id(invitem['item_file_id'])
                    value += item_ob_id.value
                    count += 1
                    await cmd.db.del_from_inventory(message.author.id, invitem['item_id'])
                await cmd.db.add_resource(message.author.id, 'currency', value, cmd.name, message)
                ender = 's' if count != 1 else ''
                response = discord.Embed(color=0xc6e4b5)
                response.title = f'💶 You sold {count} item{ender} for {value} {currency}.'
            else:
                item_o = item_core.get_item_by_name(lookup)
                if item_o:
                    item = await cmd.db.get_inventory_item(message.author.id, item_o.file_id)
                else:
                    item = None
                if item:
                    value = item_o.value
                    await cmd.db.add_resource(message.author.id, 'currency', value, cmd.name, message)
                    await cmd.db.del_from_inventory(message.author.id, item['item_id'])
                    response = discord.Embed(color=0xc6e4b5)
                    response.title = f'💶 You sold the {item_o.name} for {value} {currency}.'
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty...')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
    await message.channel.send(embed=response)
