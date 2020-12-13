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
from sigma.modules.minigames.professions.market.marketsell import MARKET_TAX_PERCENT
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.utils.ongoing.ongoing import is_ongoing, set_ongoing, del_ongoing


async def marketbuy(cmd, pld):
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
        if pld.args:
            if not is_ongoing(cmd.name, pld.msg.author.id):
                set_ongoing(cmd.name, pld.msg.author.id)
                ic = await get_item_core(cmd.db)
                lookup = ' '.join(pld.args)
                check_token = len(pld.args) == 1
                item = ic.get_item_by_name(lookup)
                if check_token and item is None:
                    me = await MarketEntry.find(cmd.db, token=lookup)
                    if me:
                        item = ic.get_item_by_file_id(me.item)
                else:
                    if item is not None:
                        me = await MarketEntry.find(cmd.db, item=item.file_id)
                    else:
                        me = None
                if me:
                    await me.delete(cmd.db)
                    self_buy = me.uid == pld.msg.author.id
                    curr = cmd.bot.cfg.pref.currency
                    action = 'Retract' if self_buy else 'Buy'
                    questitle = f'❔ {action} the {item.rarity_name} {item.name} for {me.price} {curr}?'
                    stamp = arrow.get(me.stamp).format('DD. MMM. YYYY HH:mm:ss')
                    quesbed = discord.Embed(color=0xf9f9f9, title=questitle)
                    quesbed.description = f'Market entry {me.token} submitted by {me.uname} on {stamp}.'
                    if self_buy:
                        quesbed.set_footer(text="Retracting the item does not pay its price or tax.")
                    buy_confirm, _ = await bool_dialogue(cmd.bot, pld.msg, quesbed, False)
                    if buy_confirm:
                        kud = (await cmd.db.get_resource(pld.msg.author.id, 'currency')).current
                        if self_buy:
                            data_for_inv = item.generate_inventory_item()
                            await cmd.db.add_to_inventory(pld.msg.author.id, data_for_inv)
                            response = ok(f'Retracted the {item.rarity_name} {item.name}.')
                        else:
                            if kud >= me.price:
                                await cmd.db.del_resource(pld.msg.author.id, 'currency', me.price, cmd.name, pld.msg)
                                profit = int(me.price * (1 - (MARKET_TAX_PERCENT / 100)))
                                await cmd.db.add_resource(me.uid, 'currency', profit, cmd.name, pld.msg, ranked=False)
                                await cmd.db.add_resource(
                                    cmd.bot.user.id, 'currency', me.price - profit, cmd.name, pld.msg, ranked=False
                                )
                                data_for_inv = item.generate_inventory_item()
                                await cmd.db.add_to_inventory(pld.msg.author.id, data_for_inv)
                                response = ok(f'Purchased the {item.rarity_name} {item.name} for {me.price} {curr}.')
                            else:
                                await me.save(cmd.db)
                                response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {curr}.')
                    else:
                        response = discord.Embed(color=0xbe1931, title='❌ Purchase cancelled.')
                else:
                    response = not_found('Couldn\'t find any entries for that.')
                if is_ongoing(cmd.name, pld.msg.author.id):
                    del_ongoing(cmd.name, pld.msg.author.id)
            else:
                response = error('You already have a market purchase open.')
        else:
            response = error('Not enough arguments, I need a price and item name.')
    else:
        response = error('Sorry, your account is too young to use the market.')
    await pld.msg.channel.send(embed=response)
