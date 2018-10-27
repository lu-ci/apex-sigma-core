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


async def fish(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    item_core = await get_item_core(cmd.db)
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
        upgrade_file = pld.profile.get('upgrades') or {}
        inv = await cmd.db.get_inventory(message.author.id)
        storage = upgrade_file.get('storage', 0)
        inv_limit = 64 + (8 * storage)
        if len(inv) < inv_limit:
            base_cooldown = 60
            stamina = upgrade_file.get('stamina', 0)
            cooldown = int(base_cooldown - ((base_cooldown / 100) * ((stamina * 0.5) / (1.25 + (0.01 * stamina)))))
            cooldown = 5 if cooldown < 5 else cooldown
            await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, cooldown)
            rarity = await item_core.roll_rarity(pld.profile)
            if args:
                if message.author.id in cmd.bot.cfg.dsc.owners:
                    try:
                        if int(args[0]) <= 9:
                            rarity = int(args[0])
                        else:
                            pass
                    except TypeError:
                        pass
            item = item_core.pick_item_in_rarity('fish', rarity)
            connector = 'a'
            if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            if rarity == 0:
                if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response_title = f'{item.icon} You caught {connector} {item.name} and threw it away!'
            else:
                response_title = f'{item.icon} You caught {connector} {item.rarity_name} {item.name}!'
                data_for_inv = item.generate_inventory_item()
                await cmd.db.add_to_inventory(message.author.id, data_for_inv)
                await item_core.add_item_statistic(cmd.db, item, message.author)
                await cmd.db.add_resource(message.author.id, 'items', 1, cmd.name, message, True)
            response = discord.Embed(color=item.color, title=response_title)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Your inventory is full.')
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
        response = discord.Embed(color=0x696969, title=f'🕙 Your new bait will be ready in {timeout} seconds.')
    response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
    await message.channel.send(embed=response)
