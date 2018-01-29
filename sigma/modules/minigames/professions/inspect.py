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

from .nodes.item_core import ItemCore

item_core = None


async def inspect(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        inv = await cmd.db.get_inventory(message.author)
        if inv:
            lookup = ' '.join(args)
            item_o = item_core.get_item_by_name(lookup)
            if item_o:
                item = await cmd.db.get_inventory_item(message.author, item_o.file_id)
            else:
                item = None
            if item:
                response = item_o.make_inspect_embed(cmd.bot.cfg.pref.currency)
                response.set_footer(text=f'ItemID: {item["item_id"]}')
            else:
                response = None
        else:
            response = None
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    if response:
        await message.channel.send(embed=response)
    else:
        await cmd.bot.modules.commands.get('finditem').execute(message, args)
