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
from sigma.modules.minigames.professions.nodes.item_core import ItemCore

item_core = None


async def generateitem(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore('sigma/modules/minigames/professions/res/data')
    if args:
        if message.mentions:
            if len(args) >= 2:
                target = message.mentions[0]
                lookup = ' '.join(args[1:])
                item = item_core.get_item_by_name(lookup)
                if item:
                    connector = 'a'
                    if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'an'
                    data_for_inv = item.generate_inventory_item()
                    await cmd.db.add_to_inventory(target, data_for_inv)
                    success_text = f'{item.icon} I have given {connector} {item.name} to {target.display_name}.'
                    response = discord.Embed(color=item.color, title=success_text)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 {lookup} not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
