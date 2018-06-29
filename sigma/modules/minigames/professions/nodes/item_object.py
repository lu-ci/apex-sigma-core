# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import secrets

import discord

from sigma.modules.minigames.professions.nodes.properties import rarity_names, item_icons, item_colors, cook_icons, \
    cook_colors


class SigmaRawItem(object):
    def __init__(self, item_data):
        self.name = item_data['name']
        self.desc = item_data['description']
        self.rarity = item_data['rarity']
        self.type = item_data['type']
        self.rarity_name = rarity_names[self.rarity]
        self.icon = item_icons[self.type.lower()][self.rarity]
        self.color = item_colors[self.type.lower()][self.rarity]
        self.value = item_data['value']
        self.file_id = item_data['file_id']

    def make_inspect_embed(self, currency):
        connector = 'A'
        if self.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
            connector = 'An'
        item_info = f'{connector} **{self.rarity_name.title()} {self.type.title()}**'
        item_info += f'\nIt is valued at **{self.value} {currency}**'
        response = discord.Embed(color=self.color)
        response.add_field(name=f'{self.icon} {self.name}', value=f'{item_info}')
        response.add_field(name='Item Description', value=f'{self.desc}', inline=False)
        return response

    def generate_inventory_item(self):
        token = secrets.token_hex(16)
        data = {
            'item_id': token,
            'item_file_id': self.file_id
        }
        return data


class SigmaCookedItem(object):
    def __init__(self, item_data):
        self.name = item_data['name']
        self.desc = item_data['description']
        self.type = item_data['type']
        self.icon = cook_icons[self.type.lower()]
        self.color = cook_colors[self.type.lower()]
        self.value = item_data['value']
        self.file_id = item_data['file_id']
        self.rarity = 11
        self.rarity_name = rarity_names[self.rarity]

    def make_inspect_embed(self, currency):
        connector = 'A'
        if self.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
            connector = 'An'
        item_info = f'{connector} **{self.name}** {self.type}'
        item_info += f'\nIt is valued at **{self.value} {currency}**'
        response = discord.Embed(color=self.color)
        response.add_field(name=f'{self.icon} {self.name}', value=f'{item_info}')
        response.add_field(name='Item Description', value=f'{self.desc}', inline=False)
        return response

    @staticmethod
    def roll_quality():
        roll_num = secrets.randbelow(100)
        if roll_num in range(66, 85):
            quality = 1
        elif roll_num in range(86, 95):
            quality = 2
        elif roll_num in range(96, 100):
            quality = 3
        else:
            quality = 0
        return quality

    def generate_inventory_item(self):
        token = secrets.token_hex(16)
        data = {
            'item_id': token,
            'quality': self.roll_quality(),
            'item_file_id': self.file_id
        }
        return data
