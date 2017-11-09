import discord

from .nodes.item_core import ItemCore

item_core = None


async def sell(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    currency = cmd.bot.cfg.pref.currency
    if args:
        inv = cmd.db.get_inventory(message.author)
        if inv:
            lookup = ' '.join(args)
            if lookup == 'all':
                value = 0
                count = 0
                for invitem in inv:
                    item_ob_id = item_core.get_item_by_file_id(invitem['item_file_id'])
                    value += item_ob_id.value
                    count += 1
                    cmd.db.del_from_inventory(message.author, invitem['item_id'])
                cmd.db.add_currency(message.author, message.guild, value)
                currency = cmd.bot.cfg.pref.currency
                response = discord.Embed(color=0xc6e4b5, title=f'💶 You sold {count} items for {value} {currency}.')
            else:
                item_o = item_core.get_item_by_name(lookup)
                if item_o:
                    item = cmd.db.get_inventory_item(message.author, item_o.file_id)
                else:
                    item = None
                if item:
                    value = item_o.value
                    cmd.db.add_currency(message.author, message.guild, value)
                    cmd.db.del_from_inventory(message.author, item['item_id'])
                    response = discord.Embed(color=0xc6e4b5,
                                             title=f'💶 You sold the {item_o.name} for {value} {currency}.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
