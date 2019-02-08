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

import discord
import yaml

from sigma.core.mechanics.database import Database


class AdoptableHuman(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.parents = []
        self.children = []
        self.exists = False
        self.processed = []

    async def new(self, db: Database, user: discord.Member):
        self.id = user.id
        self.name = user.name
        await self.save(db, True)

    async def load(self, db: Database, user_id: int):
        family = await db[db.db_nam].Families.find_one({'user_id': user_id})
        if family:
            self.exists = True
            self.id = user_id
            self.name = family.get('user_name')
            await self.load_iterable(db, family.get('parents', []), self.parents, self.processed)
            await self.load_iterable(db, family.get('children', []), self.children, self.processed)

    @staticmethod
    async def load_iterable(db: Database, iterable: list, appendable: list, processed: list):
        for iter_item in iterable:
            if iter_item not in processed:
                processed.append(iter_item)
                human_object = AdoptableHuman()
                human_object.processed = processed
                await human_object.load(db, iter_item)
                appendable.append(human_object)

    async def save(self, db: Database, new=False):
        data = self.to_dict()
        if new or not self.exists:
            await db[db.db_nam].Families.insert_one(data)
        else:
            await db[db.db_nam].Families.update_one({'user_id': self.id}, {'$set': data})

    def is_parent(self, user_id: int):
        confirmed = False
        if self.id == user_id:
            confirmed = True
        else:
            for parent in self.parents:
                if parent.is_parent(user_id):
                    confirmed = True
                    break
        return confirmed

    def is_child(self, user_id: int):
        confirmed = False
        if self.id == user_id:
            confirmed = True
        else:
            for child in self.children:
                if child.is_child(user_id):
                    confirmed = True
                    break
        return confirmed

    def top_parent(self):
        top = None
        if len(self.parents) == 0:
            top = self
        else:
            for parent in self.parents:
                top = parent.top_parent()
                if top:
                    break
        return top

    def bot_child(self):
        bot = None
        if len(self.children) == 0:
            bot = self
        else:
            for child in self.children:
                bot = child.bot_child()
                if bot:
                    break
        return bot

    def to_tree(self, origin: int, start=True):
        if start:
            top_parent = self.top_parent()
            return top_parent.to_tree(origin, False)
        else:
            name = self.name if self.id != origin else f'> {self.name} <'
            children = [c.to_tree(origin, False) for c in self.children]
            return {name: children}

    def draw_tree(self):
        tree_out = f'cache/family_{self.id}.yml'
        tree_data = self.to_tree(self.id)
        with open(tree_out, 'w', encoding='utf-8') as tree_file:
            yaml.safe_dump(tree_data, tree_file, default_flow_style=False)
        return tree_out

    def to_dict(self):
        return {
            'user_id': self.id,
            'user_name': self.name,
            'parents': [par.id for par in self.parents],
            'children': [cld.id for cld in self.children]
        }
