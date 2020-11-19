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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def bazaarstatistics(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    total_spent = 0
    total_markup = 0
    total_value = 0
    item_counts = {}
    currency = cmd.bot.cfg.pref.currency
    item_core = await get_item_core(cmd.db)
    total = '--total' in pld.args
    if total:
        target = None
        lookup = {}
    else:
        target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
        lookup = {'user_id': target.id}
    count = await cmd.db[cmd.db.db_nam].BazaarPurchases.count_documents(lookup)
    if count:
        most_expensive = None
        docs = cmd.db[cmd.db.db_nam].BazaarPurchases.find(lookup)
        async for doc in docs:
            item = item_core.get_item_by_file_id(doc.get('item'))
            item_count = item_counts.get(item.file_id, 0)
            item_count += 1
            item_counts.update({item.file_id: item_count})
            buy_price = doc.get('price')
            total_spent += buy_price
            total_markup += buy_price - item.value
            total_value += item.value
            if most_expensive is None:
                most_expensive = doc
            else:
                if doc.get('price') > most_expensive.get('price'):
                    most_expensive = doc
        mex_item = item_core.get_item_by_file_id(most_expensive.get('item'))
        mex_price = most_expensive.get('price')
        bought_keys = list(item_counts.keys())
        by_buy_count = list(sorted(bought_keys, key=lambda x: item_counts.get(x), reverse=True))
        most_bought = item_core.get_item_by_file_id(by_buy_count[0])
        mb_count = item_counts.get(most_bought.file_id)
        block = f"Purchases: **{count}**"
        block += f"\nCurrency Spent: **{total_spent} {currency}**"
        block += f"\nMarkup Currency Spent: **{total_markup} {currency}**"
        block += f"\nAverage Markup: **{round(total_markup / count, 2)} {currency}**"
        block += f"\nAverage Markup Multiplier: **x{round(total_spent / total_value, 2)}**"
        block += f"\nMost Bought Item: {most_bought.icon} **{most_bought.name}** ({mb_count})"
        block += f"\nMost Expensive Item: {mex_item.icon} **{mex_item.name}** ({mex_price} {currency})"
        response = discord.Embed(color=0xffac33, title='🪙 Bazaar Statistics')
        response.description = block
        if not total:
            response.set_author(name=target.display_name, icon_url=user_avatar(target))
    else:
        if total:
            response = error("Nobody has not been to the bazaar.")
        else:
            response = error(f"{target.name} has not been to the bazaar.")
    await pld.msg.channel.send(embed=response)
