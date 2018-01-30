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


async def finditem(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        lookup = ' '.join(args)
        item = item_core.get_item_by_name(lookup)
        if item:
            response = item.make_inspect_embed(cmd.bot.cfg.pref.currency)
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
