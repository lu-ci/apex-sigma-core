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
from sigma.core.utilities.dialogue_controls import item_dialogue
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.properties import item_icons


async def forage(cmd: SigmaCommand, pld: CommandPayload):
    item_core = await get_item_core(cmd.db)
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
        inv = await cmd.db.get_inventory(pld.msg.author.id)
        storage = upgrade_file.get('storage', 0)
        inv_limit = 64 + (8 * storage)
        if len(inv) < inv_limit:
            base_cooldown = 60
            stamina = upgrade_file.get('stamina', 0)
            cooldown = int(base_cooldown - ((base_cooldown / 100) * ((stamina * 0.5) / (1.25 + (0.01 * stamina)))))
            cooldown = 5 if cooldown < 5 else cooldown
            await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, cooldown)
            rarity = await item_core.roll_rarity(await cmd.bot.db.get_profile(pld.msg.author.id))
            if pld.args:
                if pld.msg.author.id in cmd.bot.cfg.dsc.owners:
                    try:
                        if int(pld.args[0]) <= 9:
                            rarity = int(pld.args[0])
                        else:
                            pass
                    except TypeError:
                        pass
            item = item_core.pick_item_in_rarity('plant', rarity)
            connector = 'a'
            if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            if rarity == 0:
                if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response_title = f'{item.icon} You found {connector} {item.name} and threw it away!'
                response = discord.Embed(color=item.color, title=response_title)
            else:
                success, timed_out = await item_dialogue(cmd.bot, pld.msg, item_icons.get(item.type.lower()), item)
                if success:
                    response_title = f'{item.icon} You found {connector} {item.rarity_name} {item.name}!'
                    data_for_inv = item.generate_inventory_item()
                    await cmd.db.add_to_inventory(pld.msg.author.id, data_for_inv)
                    await item_core.add_item_statistic(cmd.db, item, pld.msg.author)
                    await cmd.db.add_resource(pld.msg.author.id, 'items', 1, cmd.name, pld.msg, True)
                    response = discord.Embed(color=item.color, title=response_title)
                else:
                    if timed_out:
                        response_title = f'🕙 You forgot where the {item.rarity_name} {item.type.lower()} is...'
                        response = discord.Embed(color=0x696969, title=response_title)
                    else:
                        response_title = f'❌ Oh no... You dug too hard and hurt the plant...'
                        response = discord.Embed(color=0xBE1931, title=response_title)
        else:
            response = error('Your inventory is full.')
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You are resting for another {timeout} seconds.')
    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
