import os
import secrets

import discord
import yaml

from sigma.core.utilities.data_processing import user_avatar
from .item_object import SigmaRawItem, SigmaCookedItem
from .properties import rarity_names, item_colors, item_icons


class ItemCore(object):
    def __init__(self, item_directory):
        self.base_dir = item_directory
        self.rarity_names = rarity_names
        self.item_icons = item_icons
        self.item_colors = item_colors
        self.all_items = []
        self.init_items()

    def get_item_by_name(self, name):
        output = None
        for item in self.all_items:
            if item.name.lower() == name.lower():
                output = item
                break
        return output

    def get_item_by_file_id(self, name):
        output = None
        for item in self.all_items:
            if item.file_id == name:
                output = item
                break
        return output

    def pick_item_in_rarity(self, item_category, rarity):
        in_rarity = []
        for item in self.all_items:
            if item.type.lower() == item_category:
                if item.rarity == rarity:
                    in_rarity.append(item)
        choice = secrets.choice(in_rarity)
        return choice

    def init_items(self):
        raw_item_types = ['fish', 'plant', 'animal']
        cooked_item_types = ['drink', 'meal', 'desert']
        for root, dirs, files in os.walk(f'{self.base_dir}'):
            for file in files:
                if file.endswith('.yml'):
                    file_path = (os.path.join(root, file))
                    with open(file_path, encoding='utf-8') as item_file:
                        item_id = file.split('.')[0]
                        item_data = yaml.safe_load(item_file)
                        item_data.update({'file_id': item_id})
                        if item_data['type'].lower() in raw_item_types:
                            item_object = SigmaRawItem(item_data)
                        elif item_data['type'].lower() in cooked_item_types:
                            item_object = SigmaCookedItem(item_data)
                        else:
                            item_object = None
                        if item_object:
                            self.all_items.append(item_object)

    @staticmethod
    def roll_rarity(db, uid):
        upgrade_id = 'luck'
        upgrade_file = db[db.db_cfg.database].Upgrades.find_one({'UserID': uid})
        if upgrade_file is None:
            db[db.db_cfg.database].Upgrades.insert_one({'UserID': uid})
            upgrade_file = {}
        if upgrade_id in upgrade_file:
            upgrade_level = upgrade_file[upgrade_id]
        else:
            upgrade_level = 0
        rarities = {
            0: 0,
            1: 350000000,
            2: 600000000,
            3: 800000000,
            4: 950000000,
            5: 990000000,
            6: 995000000,
            7: 997500000,
            8: 999000000,
            9: 999750000
        }
        roll = secrets.randbelow(1000000000) + (upgrade_level * 250) + 1
        lowest = 0
        for rarity in rarities:
            if rarities[rarity] <= roll:
                lowest = rarity
            else:
                break
        return lowest

    @staticmethod
    async def notify_channel_of_special(message, all_channels, channel_id, item):
        if channel_id:
            target = discord.utils.find(lambda x: x.id == channel_id, all_channels)
            if target:
                connector = 'a'
                if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response_title = f'{item.icon} {connector.title()} {item.rarity_name} {item.name} has been found!'
                response = discord.Embed(color=item.color, title=response_title)
                response.set_author(name=f'{message.author.display_name}', icon_url=user_avatar(message.author))
                response.set_footer(text=f'From {message.guild.name}.', icon_url=message.guild.icon_url)
                await target.send(embed=response)
