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
import copy

import discord

from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.inventory import is_ingredient
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


async def invalid_items(db, item_names):
    """
    :type db: sigma.core.mechanics.database.Database
    :type item_names: list[str]
    :rtype: list[str]
    """
    invalid = []
    ic = await get_item_core(db)
    for item_name in item_names:
        item = ic.get_item_by_name(item_name)
        if not item:
            invalid.append(item_name)
    return invalid


async def missing_items(db, uid, item_names):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type item_names: list[str]
    :rtype: list[str]
    """
    missing = []
    ic = await get_item_core(db)
    for item_name in item_names:
        item = ic.get_item_by_name(item_name)
        inv_item = await db.get_inventory_item(uid, item.file_id)
        if not inv_item:
            missing.append(item.name)
    return missing


async def get_items(db, item_names):
    """
    :type db: sigma.core.mechanics.database.Database
    :type item_names: list[str]
    :rtype: list[SigmaRawItem or SigmaCookedItem]
    """
    items = []
    ic = await get_item_core(db)
    for item_name in item_names:
        item = ic.get_item_by_name(item_name)
        if item:
            items.append(item)
    return items


def total_value(items):
    """
    :type items: list[SigmaRawItem or SigmaCookedItem]
    :rtype: int
    """
    total = 0
    for item in items:
        total += item.value
    return total


def total_taxation(items):
    """
    :type items: list[SigmaRawItem or SigmaCookedItem]
    :rtype: int
    """
    total = 0
    for item in items:
        power = item.rarity // 2.33
        total += 10 * (10 ** power)
    return int(total)


async def question_embed(cmd, oitems, ritems, ovalue, rvalue, otax, rtax):
    """
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type oitems: list[SigmaRawItem or SigmaCookedItem]
    :type ritems: list[SigmaRawItem or SigmaCookedItem]
    :type ovalue: int
    :type rvalue: int
    :type otax: int
    :type rtax: int
    :rtype: discord.Embed
    """
    rc = await get_recipe_core(cmd.db)
    curr = cmd.bot.cfg.pref.currency
    question = '❔ Do you want to proceed with this trade?'
    quesbed = discord.Embed(color=0xf9f9f9, title=question)
    offer_item_names = []
    for oitem in oitems:
        in_rec = '*' if is_ingredient(rc.recipes, oitem) else ''
        offer_item_name = f'{oitem.rarity_name.title()} **{oitem.name}**{in_rec}'
        offer_item_names.append(offer_item_name)
    offer_desc = f'{", ".join([oin for oin in offer_item_names])}.'
    offer_desc += f'\n\nTotal Value: **{ovalue} {curr}**'
    offer_desc += f'\nTotal Tax: **{rtax} {curr}**'
    receive_item_names = []
    for ritem in ritems:
        in_rec = '*' if is_ingredient(rc.recipes, ritem) else ''
        receive_item_name = f'{ritem.rarity_name.title()} **{ritem.name}**{in_rec}'
        receive_item_names.append(receive_item_name)
    receive_desc = f'{", ".join([rin for rin in receive_item_names])}.'
    receive_desc += f'\n\nTotal Value: **{rvalue} {curr}**'
    receive_desc += f'\nTotal Tax: **{otax} {curr}**'
    quesbed.add_field(name='📤 You Give', value=offer_desc, inline=False)
    quesbed.add_field(name='📥 You Receive', value=receive_desc, inline=False)
    return quesbed


async def enough_currency(db, uid, amt):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type amt: int
    :rtype: bool
    """
    return (await db.get_resource(uid, 'currency')).current >= amt


async def bad_args(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else None
    if target:
        if not target.bot:
            trade_args = ' '.join(pld.args[1:])
            if ' for ' in trade_args:
                author_sabotaged = await cmd.db.is_sabotaged(pld.msg.author.id)
                target_sabotaged = await cmd.db.is_sabotaged(target.id)
                if author_sabotaged or target_sabotaged:
                    response = GenericResponse('Trade rejected by the Chamomile guard.').error()
                else:
                    response = None
            else:
                response = GenericResponse('Invalid arguments, please check the description and example.').error()
                response.description = cmd.desc
        else:
            response = GenericResponse('Can\'t trade with bots.').error()
    else:
        response = GenericResponse('No user targeted.').error()
    return response


async def enough_space(db, uid, items):
    inv = await db.get_inventory(uid)
    inv_limit = 128
    return len(inv) + len(items) <= inv_limit


async def add_items(db, uid, items):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type items: list[SigmaRawItem or SigmaCookedItem]
    """
    for item in items:
        await db.add_to_inventory(uid, item.generate_inventory_item())


async def del_items(db, uid, items):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type items: list[SigmaRawItem or SigmaCookedItem]
    """
    for item in items:
        inv_item = await db.get_inventory_item(uid, item.file_id)
        if inv_item:
            await db.del_from_inventory(uid, inv_item['item_id'])


async def pay_tax(cmd, pld, uid, tax):
    """
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type uid: int
    :type tax: int
    """
    await cmd.db.del_resource(uid, 'currency', tax, cmd.name, pld.msg)


async def final_checks(cmd, pld, target, oin, rin, otax, rtax):
    missing_offer = len(await missing_items(cmd.db, pld.msg.author.id, oin)) == 0
    missing_receive = len(await missing_items(cmd.db, target.id, rin)) == 0
    offer_money = await enough_currency(cmd.db, pld.msg.author.id, rtax)
    receive_money = await enough_currency(cmd.db, target.id, otax)
    return missing_offer and missing_receive and offer_money and receive_money


async def trade(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    response = await bad_args(cmd, pld)
    if response is None:
        target = pld.msg.mentions[0] if pld.msg.mentions else None
        trade_args = ' '.join(pld.args[1:])
        for_args = trade_args.split('for')
        offer_str = for_args[0].strip()
        receive_str = for_args[1].strip()
        offer_item_names = [oi.strip() for oi in offer_str.split(',')]
        receive_item_names = [ri.strip() for ri in receive_str.split(',')]
        invalid_offer = await invalid_items(cmd.db, offer_item_names)
        invalid_receive = await invalid_items(cmd.db, receive_item_names)
        if not invalid_offer and not invalid_receive:
            missing_offer = await missing_items(cmd.db, pld.msg.author.id, offer_item_names)
            missing_receive = await missing_items(cmd.db, target.id, receive_item_names)
            if not missing_offer and not missing_receive:
                offer_items = await get_items(cmd.db, offer_item_names)
                receive_items = await get_items(cmd.db, receive_item_names)
                offer_value = total_value(offer_items)
                receive_value = total_value(receive_items)
                offer_tax = total_taxation(offer_items)
                receive_tax = total_taxation(receive_items)
                offer_question = await question_embed(
                    cmd, offer_items, receive_items, offer_value, receive_value, offer_tax, receive_tax
                )
                offer_dialogue = DialogueCore(cmd.bot, pld.msg, offer_question)
                odresp = await offer_dialogue.bool_dialogue()
                if odresp.ok:
                    receive_question = await question_embed(
                        cmd, receive_items, offer_items, receive_value, offer_value, receive_tax, offer_tax
                    )
                    fake_msg = copy.copy(pld.msg)
                    fake_msg.author = target
                    receive_dialogue = DialogueCore(cmd.bot, fake_msg, receive_question)
                    rdresp = await receive_dialogue.bool_dialogue()
                    if rdresp.ok:
                        offer_money = await enough_currency(cmd.db, pld.msg.author.id, receive_tax)
                        receive_money = await enough_currency(cmd.db, target.id, offer_tax)
                        if offer_money and receive_money:
                            offer_space = await enough_space(cmd.db, pld.msg.author.id, receive_items)
                            receive_space = await enough_space(cmd.db, target.id, offer_items)
                            if offer_space and receive_space:
                                final_check = await final_checks(
                                    cmd, pld, target, offer_item_names, receive_item_names, offer_tax, receive_tax
                                )
                                if final_check:
                                    await pay_tax(cmd, pld, pld.msg.author.id, receive_tax)
                                    await pay_tax(cmd, pld, target.id, offer_tax)
                                    await del_items(cmd.db, pld.msg.author.id, offer_items)
                                    await add_items(cmd.db, target.id, offer_items)
                                    await del_items(cmd.db, target.id, receive_items)
                                    await add_items(cmd.db, pld.msg.author.id, receive_items)
                                    response = GenericResponse('Trade complete.').ok()
                                else:
                                    response = GenericResponse(
                                        'Final checks failed, please restart the trade.'
                                    ).error()
                            else:
                                response = GenericResponse(
                                    'One or both of you don\'t have enough inventory space.'
                                ).error()
                        else:
                            response = GenericResponse('One or both of you can\'t pay required the tax.').error()
                    else:
                        response = rdresp.generic('trade response')
                else:
                    response = odresp.generic('trade request')
            else:
                response = GenericResponse('I couldn\'t find some of the items in your inventories.').error()
                response.description = ''
                if missing_offer:
                    response.description += f'\nMissing Offered Items: **{", ".join(missing_offer)}**.'
                if missing_receive:
                    response.description += f'\nMissing Requested Items: **{", ".join(missing_receive)}**.'
        else:
            response = GenericResponse('I couldn\'t find some of the items.').error()
            response.description = ''
            if invalid_offer:
                response.description += f'\nInvalid Offered Items: **{", ".join(invalid_offer)}**.'
            if invalid_receive:
                response.description += f'\nInvalid Requested Items: **{", ".join(invalid_receive)}**.'
    await pld.msg.channel.send(embed=response)
