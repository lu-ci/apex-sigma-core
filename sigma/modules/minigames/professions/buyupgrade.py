"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.dialogue_controls import int_dialogue
from sigma.core.utilities.generic_responses import error, ok
from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list
from sigma.modules.minigames.utils.ongoing.ongoing import del_ongoing, is_ongoing, set_ongoing


def get_price_mod(base_price, upgrade_level):
    """
    Gets the level-based price modifier of an upgrade.
    :param base_price: The base price of the upgrade.
    :type base_price: int
    :param upgrade_level: The wanted level of the upgrade.
    :type upgrade_level:int
    :return:
    :rtype: int
    """
    return int(base_price * upgrade_level * (1.10 + (0.075 * upgrade_level)))


def get_price(base_price, upgrade_level):
    """
    Gets the total price of an upgrade based on its level.
    :param base_price: The base price of the upgrade.
    :type base_price: int
    :param upgrade_level: The wanted level of the upgrade.
    :type upgrade_level: int
    :return:
    :rtype: int
    """
    if upgrade_level == 0:
        upgrade_price = base_price
    else:
        price_mod = get_price_mod(base_price, upgrade_level)
        upgrade_price = price_mod + (price_mod // 2)
    return upgrade_price


async def buyupgrade(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    choice = None
    if pld.args:
        try:
            choice = upgrade_list[abs(int(pld.args[0])) - 1]
        except (IndexError, ValueError):
            for upgrade in upgrade_list:
                qry = pld.args[0].lower()
                if upgrade.get('id') == qry:
                    choice = upgrade
                    break
                elif qry in upgrade.get('name').lower() and len(qry) >= 3:
                    choice = upgrade
                    break
    if choice:
        await quick_buy(cmd, pld, choice)
    else:
        await slow_buy(cmd, pld)


async def quick_buy(cmd: SigmaCommand, pld: CommandPayload, choice: dict):
    """

    :param cmd:
    :type cmd:
    :param pld:
    :type pld:
    :param choice:
    :type choice:
    """
    currency = cmd.bot.cfg.pref.currency
    user_upgrades = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
    upgrade_level = user_upgrades.get(choice.get('id'), 0)
    upgrade_price = get_price(choice.get("cost"), upgrade_level)
    current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
    current_kud = current_kud.current
    if current_kud >= upgrade_price:
        user_upgrades.update({choice.get('id'): upgrade_level + 1})
        await cmd.db.set_profile(pld.msg.author.id, 'upgrades', user_upgrades)
        await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
        response = ok(f'Upgraded your {choice.get("name")} to Level {upgrade_level + 1}.')
    else:
        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
    await pld.msg.channel.send(embed=response)


async def slow_buy(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    currency = cmd.bot.cfg.pref.currency
    if not is_ongoing(cmd.name, pld.msg.author.id):
        set_ongoing(cmd.name, pld.msg.author.id)
        upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
        upgrade_text = ''
        upgrade_index = 0
        for upgrade in upgrade_list:
            upgrade_index += 1
            upgrade_id = upgrade.get('id')
            upgrade_level = upgrade_file.get(upgrade_id, 0)
            base_price = upgrade.get('cost')
            upgrade_price = get_price(base_price, upgrade_level)
            next_upgrade = upgrade_level + 1
            upgrade_text += f'\n**{upgrade_index}**: Level {next_upgrade} {upgrade["name"]}'
            upgrade_text += f' - {upgrade_price} {currency}'
            upgrade_text += f'\n > {upgrade["desc"]}'
        upgrade_list_embed = discord.Embed(color=0xF9F9F9, title='🛍 Profession Upgrade Shop')
        upgrade_list_embed.description = upgrade_text
        upgrade_list_embed.set_footer(text='Please input the number of the upgrade you want.')
        upgrade_number, timeout = await int_dialogue(cmd.bot, pld.msg, upgrade_list_embed, 1, len(upgrade_list))
        if not timeout:
            upgrade = upgrade_list[upgrade_number - 1]
            current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
            current_kud = current_kud.current
            upgrade_id = upgrade['id']
            upgrade_level = upgrade_file.get(upgrade_id, 0)
            base_price = upgrade['cost']
            upgrade_price = get_price(base_price, upgrade_level)
            if current_kud >= upgrade_price:
                new_upgrade_level = upgrade_level + 1
                upgrade_file.update({upgrade_id: new_upgrade_level})
                await cmd.db.set_profile(pld.msg.author.id, 'upgrades', upgrade_file)
                await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
                response = ok(f'Upgraded your {upgrade["name"]} to Level {new_upgrade_level}.')
            else:
                response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
        else:
            response = discord.Embed(color=0x696969, title='🕙 Sorry, you timed out.')
        if is_ongoing(cmd.name, pld.msg.author.id):
            del_ongoing(cmd.name, pld.msg.author.id)
    else:
        response = error('You already have a shop open.')
    await pld.msg.channel.send(embed=response)
