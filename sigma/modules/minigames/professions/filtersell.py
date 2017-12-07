import discord

from .nodes.item_core import ItemCore

item_core = None


async def sell_item_ids(db, user, items):
    inv = await db.get_inventory(user)
    for item in items:
        for inv_item in inv:
            if inv_item['item_id'] == item:
                inv.remove(inv_item)
    await db.update_inv(user, inv)


async def filtersell(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        full_qry = ' '.join(args)
        arguments = full_qry.split(':')
        if len(arguments) >= 2:
            mode = arguments[0].lower()
            lookup = ' '.join(arguments[1:])
            inv = await cmd.db.get_inventory(message.author)
            if inv:
                sell_count = 0
                sell_value = 0
                if mode == 'name':
                    attribute = 'name'
                elif mode == 'type':
                    attribute = 'type'
                elif mode == 'rarity' or mode == 'quality':
                    attribute = 'rarity_name'
                else:
                    attribute = None
                if attribute:
                    sell_id_list = []
                    for item in inv:
                        item_ob_id = item_core.get_item_by_file_id(item['item_file_id'])
                        item_attribute = getattr(item_ob_id, attribute)
                        if item_attribute.lower() == lookup.lower():
                            sell_value += item_ob_id.value
                            sell_count += 1
                            sell_id_list.append(item['item_id'])
                    sell_item_ids(cmd.db, message.author, sell_id_list)
                    await cmd.db.add_currency(message.author, message.guild, sell_value)
                    currency = cmd.bot.cfg.pref.currency
                    sell_title = f'💶 You sold {sell_count} items for {sell_value} {currency}.'
                    response = discord.Embed(color=0xc6e4b5, title=sell_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid arguments.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Your inventory is empty.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
