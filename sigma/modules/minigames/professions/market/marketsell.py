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

from sigma.core.utilities.dialogue_controls import bool_dialogue
from sigma.core.utilities.generic_responses import error, not_found, ok
from sigma.modules.minigames.professions.market.market_models import MarketEntry
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.utils.ongoing.ongoing import set_ongoing, is_ongoing, del_ongoing

MARKET_TAX_PERCENT = 5


async def marketsell(cmd, pld):
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
                    if not is_ongoing(cmd.name, pld.msg.author.id):
                        set_ongoing(cmd.name, pld.msg.author.id)
                        inv_item = await cmd.db.get_inventory_item(pld.msg.author.id, item.file_id)
                        if inv_item:
                            curr = cmd.bot.cfg.pref.currency
                            profit = int(price * (1 - (MARKET_TAX_PERCENT / 100)))
                            questitle = f'❔ Sell the {item.rarity_name} {item.name} for {price} {curr}?'
                            quesbed = discord.Embed(color=0xf9f9f9, title=questitle)
                            desc = f'The market has a {MARKET_TAX_PERCENT}% tax so if your item gets sold,'
                            desc += f' you will get {profit} instead of {price} {curr}.'
                            desc += ' Retratcing the item is not taxed.'
                            quesbed.description = desc
                            sell_confirm, _ = await bool_dialogue(cmd.bot, pld.msg, quesbed, False)
                            if sell_confirm:
                                me = MarketEntry.new(pld.msg.author, item.file_id, price)
                                await me.save(cmd.db)
                                await cmd.db.del_from_inventory(pld.msg.author.id, inv_item['item_id'])
                                pfx = cmd.db.get_prefix(pld.settings)
                                desc = f'Placed the {item.rarity_name} {item.name} on the market for {price} {curr}.'
                                desc += f' Your market entry token is `{me.token}`, it can be bought directly using the'
                                desc += f' `{pfx}marketbuy {me.token}` command.'
                                response = ok('Market entry created.')
                                response.description = desc
                            else:
                                response = discord.Embed(color=0xbe1931, title='❌ Sale cancelled.')
                        else:
                            response = not_found('You don\'t have this item in your inventory.')
                        if is_ongoing(cmd.name, pld.msg.author.id):
                            del_ongoing(cmd.name, pld.msg.author.id)
                    else:
                        response = error('You already have a market sale open.')
                else:
                    response = not_found('Couldn\'t find that item, did you spell the name correctly?')
            else:
                response = error('Invalid arguments.')
                response.description = 'Place the price first, and the item name after that.'
        else:
            response = error('Not enough arguments, I need a price and item name.')
    else:
        response = error('Sorry, your account is too young to use the market.')
    await pld.msg.channel.send(embed=response)
