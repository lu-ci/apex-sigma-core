import discord

from sigma.modules.minigames.professions.nodes.item_core import ItemCore

item_core = None


async def destroyitem(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore('sigma/modules/minigames/professions/res/data')
    if args:
        id_lookup = args[0]
        inv_item = await cmd.db[cmd.db.db_cfg.database].Inventory.find_one({'Items.item_id': id_lookup})
        if inv_item:
            target = discord.utils.find(lambda x: x.id == inv_item['UserID'], cmd.bot.get_all_members())
            item_data = None
            for item in inv_item['Items']:
                if item['item_id'] == id_lookup:
                    item_data = item
                    break
            item_id = item_data['item_id']
            item_file_id = item_data['item_file_id']
            await cmd.db.del_from_inventory(target, item_id)
            item_o = item_core.get_item_by_file_id(item_file_id)
            connector = 'a'
            if item_o.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            success_text = f'{item_o.icon} I have removed {connector} {item_o.name} from {target.display_name}.'
            response = discord.Embed(color=item_o.color, title=success_text)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No item with that ID was found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
