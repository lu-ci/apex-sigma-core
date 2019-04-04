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
import yaml

from sigma.core.mechanics.database import Database
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name


class AdoptableHuman(object):
    def __init__(self, db: Database, user_id: int, parents_only=False, children_only=False):
        self.id = user_id
        self.db = db
        self.data = {}
        self.name = None
        self.parents = []
        self.children = []
        self.exists = False
        self.parents_only = parents_only
        self.children_only = children_only

    async def new(self, user: discord.Member):
        self.id = user.id
        self.name = clean_name(user.name, str(self.id))
        await self.save(True)

    async def load(self):
        family = await self.db[self.db.db_nam].Families.find_one({'user_id': self.id})
        if family:
            self.data = family
            self.exists = True
            self.name = clean_name(family.get('user_name'), str(self.id))
            if not self.children_only:
                await self.load_iterable(family.get('parents', []), self.parents, True, False)
            if not self.parents_only:
                await self.load_iterable(family.get('children', []), self.children, False, True)

    def update_name(self, name: str):
        self.name = clean_name(name, str(self.id))

    async def load_iterable(self, iterable: list, appendable: list, p_only: bool, c_only: bool):
        for iter_item in iterable:
            human_object = AdoptableHuman(self.db, iter_item, p_only, c_only)
            await human_object.load()
            appendable.append(human_object)

    async def save(self, new=False):
        self.data = self.to_dict()
        if new:
            await self.db[self.db.db_nam].Families.insert_one(self.data)
        else:
            await self.db[self.db.db_nam].Families.update_one({'user_id': self.id}, {'$set': self.data})

    async def is_related(self, human):
        child_check = self.is_child(human.id)
        parent_check = self.is_parent(human.id)
        sibling_check = self.is_sibling(human.id)
        direct = child_check or parent_check or sibling_check
        sibling = sibling_check
        ancestor = parent_check
        descendant = child_check
        if not sibling and not ancestor and not descendant:
            cousin, sd, cd, _sf, _cf = await self.is_cousin(self, human)
            if cousin:
                if sd > cd:
                    descendant = True
                elif sd < cd:
                    ancestor = True
                elif sd == cd:
                    sibling = True
        return direct, sibling, ancestor, descendant

    @staticmethod
    async def is_cousin(me, human, tp=None, sd: int = 0, cd: int = 0, sf: bool = False, cf: bool = False):
        cousin = False
        self_depth = sd
        cous_depth = cd
        self_found = sf
        cous_found = cf
        if not self_found:
            self_depth += 1
        if not cous_found:
            cous_depth += 1
        top_parent = tp
        if top_parent is None:
            top_parent = AdoptableHuman(me.db, human.top_parent().id, False, True)
            await top_parent.load()
        for child in top_parent.children:
            if not self_found:
                if child.id == me.id:
                    self_found = True
            if not cous_found:
                if child.id == human.id:
                    cous_found = True
            if not self_found or not cous_found:
                await child.is_cousin(me, human, child, self_depth, cous_depth, self_found, cous_found)
        if self_found and self_depth:
            cousin = True
        return cousin, self_depth, cous_depth, self_found, cous_found

    def is_sibling(self, user_id: int):
        sibling = False
        for parent in self.parents:
            for child in parent.data.get('children', []):
                if child == user_id:
                    sibling = True
                    break
            if sibling:
                break
        return sibling

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

    @staticmethod
    def get_break(index: int, heritage: list):
        return index == 1 or len(heritage) == 1

    def top_parent(self):
        top = None
        if len(self.parents) == 0:
            top = self
        else:
            for i, parent in enumerate(self.parents):
                top = parent.top_parent()
                if top:
                    if self.get_break(i, self.parents):
                        break
        return top

    def bot_child(self):
        bot = None
        if len(self.children) == 0:
            bot = self
        else:
            for i, child in enumerate(self.children):
                bot = child.bot_child()
                if bot:
                    if self.get_break(i, self.children):
                        break
        return bot

    def to_tree(self, origin: int):
        return {self.name: [c.to_tree(origin) for c in self.children]}

    def draw_tree(self, origin: int):
        tree_data = self.to_tree(origin)
        tree_out = yaml.safe_dump(tree_data, default_flow_style=False)
        return tree_out

    def to_dict(self):
        return {
            'user_id': self.id,
            'user_name': self.name,
            'parents': [par.id for par in self.parents],
            'children': [cld.id for cld in self.children]
        }
