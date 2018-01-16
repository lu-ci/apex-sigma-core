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
    def create_roll_range(top_roll):
        chances = {
            0: 35,
            1: 25,
            2: 20,
            3: 15,
            4: 4,
            5: 0.5,
            6: 0.25,
            7: 0.15,
            8: 0.075,
            9: 0.025
        }
        rarities = {}
        global_boundary = 0
        for rarity in chances.keys():
            if rarity == list(chances.keys())[0]:
                roll_boundary = 0
            else:
                chance = chances.get(rarity - 1) / 100
                roll_boundary = top_roll * chance
            global_boundary += roll_boundary
            rarities.update({rarity: global_boundary})
        return rarities

    async def roll_rarity(self, db, uid):
        upgrade_id = 'luck'
        upgrade_file = await db[db.db_cfg.database].Upgrades.find_one({'UserID': uid})
        if upgrade_file is None:
            await db[db.db_cfg.database].Upgrades.insert_one({'UserID': uid})
            upgrade_file = {}
        if upgrade_id in upgrade_file:
            upgrade_level = upgrade_file[upgrade_id]
        else:
            upgrade_level = 0
        top_roll = int(1000000 * (((100 - (upgrade_level * 0.5)) / 1.25) / 100))
        rarities = self.create_roll_range(top_roll)
        sabotage_file = await db[db.db_cfg.database].SabotagedUsers.find_one({'UserID': uid})
        if sabotage_file:
            roll = 0
        else:
            roll = secrets.randbelow(top_roll)
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
