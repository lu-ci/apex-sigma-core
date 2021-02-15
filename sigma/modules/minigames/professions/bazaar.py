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

import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


async def get_active_shop(db, uid):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :rtype: dict
    """
    now = arrow.utcnow().format('YYYY-MM-DD')
    doc = await db[db.db_nam].BazaarCache.find_one({'user_id': uid})
    if doc:
        doc_stamp = doc.get('date')
        if now != doc_stamp:
            doc = None
    return doc


async def generate_shop(db, uid):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :rtype: dict
    """
    data = None
    need_new = False
    doc = await db[db.db_nam].BazaarCache.find_one({'user_id': uid})
    if doc:
        now = arrow.utcnow().format('YYYY-MM-DD')
        doc_stamp = doc.get('date')
        if now != doc_stamp:
            await db[db.db_nam].BazaarCache.delete_many({'date': {'$ne': now}})
            need_new = True
    else:
        need_new = True
    if need_new:
        await db[db.db_nam].BazaarCache.delete_many({'user_id': uid})
        data = {
            'user_id': uid,
            'date': arrow.utcnow().format('YYYY-MM-DD')
        }
        item_core = await get_item_core(db)
        for key in ['fish', 'plant', 'animal']:
            pool = []
            for rarity in range(5, 10):
                item = item_core.pick_item_in_rarity(key, rarity)
                if doc:
                    if doc.get(key) != item.file_id:
                        pool.append(item.file_id)
                else:
                    pool.append(item.file_id)
            choice = pool[secrets.randbelow(len(pool))]
            data.update({key: choice})
        await db[db.db_nam].BazaarCache.insert_one(data)
    return data


async def track_purchase(db, uid, variant, item, price):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type variant:  str
    :type item: str
    :type price: int
    """
    data = {
        'date': arrow.utcnow().format('YYYY-MM-DD'),
        'user_id': uid,
        'variant': variant,
        'item': item,
        'price': price
    }
    await db[db.db_nam].BazaarPurchases.insert_one(data)


async def has_purchased(db, uid, variant):
    """
    :type db: sigma.core.mechanics.database.Database
    :type uid: int
    :type variant: str
    :rtype: bool
    """
    data = {
        'date': arrow.utcnow().format('YYYY-MM-DD'),
        'user_id': uid,
        'variant': variant
    }
    count = await db[db.db_nam].BazaarPurchases.count_documents(data)
    return count != 0


def price_multi(item_name):
    """
    :type item_name: str
    :rtype: float
    """
    now = arrow.utcnow()
    now = now.format('YY-M-D-d')
    pieces = [int(px) * 1.23 for px in now.split('-')]
    modifier = int(sum(pieces) * 100)
    divider = len(str(modifier)) - 1
    multi = modifier / (10 ** divider)
    if multi < 2:
        multi = 2
    item_sum = sum([ord(ch) for ch in item_name])
    item_modifier = int(item_sum * 100)
    item_divider = len(str(item_modifier)) - 1
    item_multi = item_modifier / (10 ** item_divider)
    return (multi + item_multi) / 1.66


async def bazaar(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    author_stamp = arrow.get(pld.msg.author.created_at).float_timestamp
    current_stamp = arrow.utcnow().float_timestamp
    time_diff = current_stamp - author_stamp
    if time_diff > 2592000:
        if not Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
            Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
            item_core = await get_item_core(cmd.db)
            doc = await get_active_shop(cmd.db, pld.msg.author.id)
            if not doc:
                doc = await generate_shop(cmd.db, pld.msg.author.id)
            currency = cmd.bot.cfg.pref.currency
            lines = []
            keys = ['fish', 'plant', 'animal']
            for (kx, key) in enumerate(keys):
                available = not await has_purchased(cmd.db, pld.msg.author.id, key)
                item = item_core.get_item_by_file_id(doc.get(key))
                if available:
                    multi = price_multi(item.file_id)
                    price = int(item.value * multi)
                    item_name = f"{item.icon} {item.rarity_name.title()} {item.name}: **{price} {currency}**"
                else:
                    item_name = f"{item.icon} ~~{item.rarity_name.title()} {item.name}~~"
                line = f"**{kx + 1}**: {item_name}"
                lines.append(line)
            question = discord.Embed(color=0xffac33, title='🪙 The Item Bazaar')
            question.description = '\n'.join(lines)
            dialogue = DialogueCore(cmd.bot, pld.msg, question)
            dresp = await dialogue.int_dialogue(1, len(keys))
            if dresp.ok and dresp.value is not None:
                key = keys[dresp.value - 1]
                item = item_core.get_item_by_file_id(doc.get(key))
                available = not await has_purchased(cmd.db, pld.msg.author.id, key)
                if available:
                    curr = (await cmd.db.get_resource(pld.msg.author.id, 'currency')).current
                    multi = price_multi(item.file_id)
                    price = int(item.value * multi)
                    if curr >= price:
                        await cmd.db.del_resource(pld.msg.author.id, 'currency', price, cmd.name, pld.msg)
                        data_for_inv = item.generate_inventory_item()
                        await cmd.db.add_to_inventory(pld.msg.author.id, data_for_inv)
                        await track_purchase(cmd.db, pld.msg.author.id, key, item.file_id, price)
                        await item_core.add_item_statistic(cmd.db, item, pld.msg.author)
                        await cmd.db.add_resource(pld.msg.author.id, 'items', 1, cmd.name, pld.msg, True)
                        response = GenericResponse(f"You have purchased a {item.name} for {price} {currency}.").ok()
                    else:
                        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
                else:
                    response = GenericResponse('One per customer please.').error()
            else:
                response = dresp.generic('bazaar')
            if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
                Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
        else:
            response = GenericResponse('You already have a bazaar open.').error()
    else:
        response = GenericResponse('Sorry, your account is too young to visit the bazaar.').error()
    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
