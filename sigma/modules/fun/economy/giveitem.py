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
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def giveitem(cmd: SigmaCommand, pld: CommandPayload):
    item_core = await get_item_core(cmd.db)
    if len(args) > 1:
        if message.mentions:
            target = message.mentions[0]
            lookup = ' '.join(args[1:])
            obj_item = item_core.get_item_by_name(lookup)
            if obj_item:
                inv_item = await cmd.db.get_inventory_item(message.author.id, obj_item.file_id)
                if inv_item:
                    upgrade_file = await cmd.db.get_profile(target.id, 'upgrades') or {}
                    inv = await cmd.db.get_inventory(target.id)
                    storage = upgrade_file.get('storage', 0)
                    inv_limit = 64 + (8 * storage)
                    author_sab = await cmd.db.is_sabotaged(message.author.id)
                    target_sab = await cmd.db.is_sabotaged(target.id)
                    if len(inv) < inv_limit:
                        if not author_sab and not target_sab:
                            await cmd.db.del_from_inventory(message.author.id, inv_item.get('item_id'))
                            inv_item.update({'transferred': True})
                            await cmd.db.add_to_inventory(target.id, inv_item)
                            await cmd.db.add_resource(target.id, 'items', 1, cmd.name, message, True)
                            title = f'✅ Transferred {obj_item.name} to {target.display_name}.'
                            response = discord.Embed(color=0x77B255, title=title)
                            response.set_footer(text=f'Item ID: {inv_item.get("item_id")}')
                        else:
                            response = discord.Embed(color=0xBE1931, title='❗ Transfer declined by Lucia\'s Guard.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ {target.name}\'s inventory is full.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 No {obj_item.name} found in your inventory.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No such item exists.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    await message.channel.send(embed=response)
