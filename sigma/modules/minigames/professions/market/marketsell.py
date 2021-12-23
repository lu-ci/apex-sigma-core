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

import arrow
import discord

from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.market.market_expiration import MARKET_LIFETIME
from sigma.modules.minigames.professions.market.market_models import MarketEntry
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

MARKET_TAX_PERCENT = 5


async def marketsell(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if await cmd.db.is_sabotaged(pld.msg.author.id):
        response = GenericResponse('Quarantined users can\'t use the market.').denied()
        await pld.msg.channel.send(embed=response)
        return
    author_stamp = arrow.get(pld.msg.author.created_at).float_timestamp
    current_stamp = arrow.utcnow().float_timestamp
    time_diff = current_stamp - author_stamp
    if time_diff > 2592000:
        if len(pld.args) >= 2:
            valid = True
            try:
                price = int(pld.args[0])
            except ValueError:
                price = 0
                valid = False
            if valid:
                ic = await get_item_core(cmd.db)
                item_lookup = ' '.join(pld.args[1:])
                item = ic.get_item_by_name(item_lookup)
                if item:
                    min_price = int(10 * (10 ** (item.rarity // 2.33)))
                    if price >= min_price:
                        if not Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
                            Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
                            inv_item = await cmd.db.get_inventory_item(pld.msg.author.id, item.file_id)
                            if inv_item:
                                expiration = arrow.get(
                                    arrow.utcnow().int_timestamp + MARKET_LIFETIME
                                ).format('DD. MMM. YYYY HH:mm UTC')
                                cost = int(price * 0.005)
                                cost = cost if cost else 10
                                curr = cmd.bot.cfg.pref.currency
                                profit = int(price * (1 - (MARKET_TAX_PERCENT / 100)))
                                questitle = f'❔ Sell the {item.rarity_name} {item.name} for {price} {curr}?'
                                quesbed = discord.Embed(color=0xf9f9f9, title=questitle)
                                desc = f'Listing the item costs **{cost}** {curr}.'
                                desc += f' The market has a {MARKET_TAX_PERCENT}% tax so if your item gets sold,'
                                desc += f' you will get {profit} instead of {price} {curr}.'
                                desc += ' Retracting the item is not taxed.'
                                desc += f' The item will be available until {expiration}.'
                                quesbed.description = desc
                                dialogue = DialogueCore(cmd.bot, pld.msg, quesbed)
                                dresp = await dialogue.bool_dialogue()
                                if dresp.ok:
                                    wallet = (await cmd.db.get_resource(pld.msg.author.id, 'currency')).current
                                    if wallet >= cost:
                                        me = MarketEntry.new(pld.msg.author, item.file_id, price)
                                        try:
                                            await me.save(cmd.db)
                                            await cmd.db.del_resource(
                                                pld.msg.author.id, 'currency', cost, cmd.name, pld.msg
                                            )
                                            await cmd.db.del_from_inventory(pld.msg.author.id, inv_item['item_id'])
                                            pfx = cmd.db.get_prefix(pld.settings)
                                            desc = f'Placed the {item.rarity_name} {item.name}'
                                            desc += f' on the market for {price} {curr}.'
                                            desc += f' The listing expiry is {expiration}.'
                                            desc += f' Your market entry token is `{me.token}`,'
                                            desc += ' it can be bought directly using the'
                                            desc += f' `{pfx}marketbuy {me.token}` command.'
                                            response = GenericResponse('Market entry created.').ok()
                                            response.description = desc
                                        except OverflowError:
                                            response = GenericResponse("Whoa, that number is way too big!").error()
                                    else:
                                        response = GenericResponse('You\'re not able to pay the listing fee.').error()
                                else:
                                    response = dresp.generic('market sale')
                            else:
                                response = GenericResponse('You don\'t have this item in your inventory.').not_found()
                            if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
                                Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
                        else:
                            response = GenericResponse('You already have a market sale open.').error()
                    else:
                        curr = cmd.bot.cfg.pref.currency
                        msg = f'{item.rarity_name.title()} items have a minimum price of {min_price} {curr}.'
                        response = GenericResponse(msg).error()
                else:
                    response = GenericResponse(
                        'Couldn\'t find that item, did you spell the name correctly?'
                    ).not_found()
            else:
                response = GenericResponse('Invalid arguments.').error()
                response.description = 'Place the price first, and the item name after that.'
        else:
            response = GenericResponse('Not enough arguments, I need a price and item name.').error()
    else:
        response = GenericResponse('Sorry, your account is too young to use the market.').error()
    await pld.msg.channel.send(embed=response)
