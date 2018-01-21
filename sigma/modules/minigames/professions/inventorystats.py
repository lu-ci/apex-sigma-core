import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.data_processing import user_avatar
from .nodes.item_core import ItemCore

item_core = None


async def inventorystats(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    inv = await cmd.db.get_inventory(target)
    item_o_list = []
    for item in inv:
        item_o = item_core.get_item_by_file_id(item['item_file_id'])
        item_o_list.append(item_o)
    item_o_list = sorted(item_o_list, key=lambda x: x.rarity, reverse=True)
    inv = item_o_list
    if inv:
        total_value = 0
        rarity_dict = {}
        type_dict = {}
        for item_o_item in item_o_list:
            total_value += item_o_item.value
            if item_o_item.type.lower() in type_dict:
                type_count = type_dict[item_o_item.type.lower()]
            else:
                type_count = 0
            type_count += 1
            type_dict.update({item_o_item.type.lower(): type_count})
            if item_o_item.rarity_name in rarity_dict:
                rare_count = rarity_dict[item_o_item.rarity_name]
            else:
                rare_count = 0
            rare_count += 1
            rarity_dict.update({item_o_item.rarity_name: rare_count})
        type_keys = ['fish', 'plant', 'animal']
        type_list = []
        for type_key in type_keys:
            if type_key in type_dict:
                type_num = type_dict[type_key]
            else:
                type_num = 0
            type_list.append([type_key.upper(), type_num])
        type_out = boop(type_list)
        rare_keys = ['common', 'uncommon', 'rare', 'legendary', 'prime',
                     'spectral', 'ethereal', 'antimatter', 'omnipotent']
        rare_list = []
        for rare_key in rare_keys:
            if rare_key in rarity_dict:
                rare_num = rarity_dict[rare_key]
            else:
                rare_num = 0
            rare_list.append([rare_key.upper(), rare_num])
        rare_out = boop(rare_list)
        response = discord.Embed(color=0xc16a4f)
        response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
        response.add_field(name='Items by Type', value=f'```py\n{type_out}\n```', inline=False)
        response.add_field(name='Items by Rarity', value=f'```py\n{rare_out}\n```', inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    await message.channel.send(embed=response)
