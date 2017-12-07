import discord

from sigma.core.utilities.data_processing import user_avatar
from .nodes.item_core import ItemCore

item_core = None


async def hunt(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
        upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': message.author.id})
        if upgrade_file is None:
            await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one({'UserID': message.author.id})
            upgrade_file = {}
        inv = await cmd.db.get_inventory(message.author)
        if 'storage' in upgrade_file:
            storage = upgrade_file['storage']
        else:
            storage = 0
        inv_limit = 64 + (8 * storage)
        if len(inv) < inv_limit:
            base_cooldown = 60
            if 'stamina' in upgrade_file:
                stamina = upgrade_file['stamina']
            else:
                stamina = 0
            cooldown = int(base_cooldown - ((base_cooldown / 100) * (stamina * 0.5)))
            await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, cooldown)
            rarity = await item_core.roll_rarity(cmd.db, message.author.id)
            if args:
                if message.author.id in cmd.bot.cfg.dsc.owners:
                    try:
                        rarity = int(args[0])
                    except TypeError:
                        pass
            if rarity == 0:
                item = None
                item_color = 0x67757f
                response_title = f'🗑 You failed to catch anything.'
            else:
                item = item_core.pick_item_in_rarity('animal', rarity)
                connector = 'a'
                if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                item_color = item.color
                response_title = f'{item.icon} You caught {connector} {item.rarity_name} {item.name}!'
                data_for_inv = item.generate_inventory_item()
                await cmd.db.add_to_inventory(message.author, data_for_inv)
            response = discord.Embed(color=item_color, title=response_title)
            response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
            if rarity >= 5:
                if 'item_channel' in cmd.cfg:
                    await item_core.notify_channel_of_special(message, cmd.bot.get_all_channels(),
                                                              cmd.cfg['item_channel'], item)
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Your inventory is full.')
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You are resting for another {timeout} seconds.')
    await message.channel.send(embed=response)
