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

import abc
import secrets

import arrow


class MarketEntry(abc.ABC):
    def __init__(self, doc=None):
        """
        :param doc:
        :type doc: dict
        """
        self.raw = doc if doc else {}
        self.token = self.raw.get('token')
        self.uid = self.raw.get('user_id')
        self.uname = self.raw.get('user_name')
        self.price = self.raw.get('price')
        self.stamp = self.raw.get('stamp')
        self.item = self.raw.get('item')

    @staticmethod
    def new(user, item, price):
        """

        :param user:
        :type user: discord.User
        :param item:
        :type item: str
        :param price:
        :type price: int
        :return:
        :rtype: MarketEntry
        """
        me = MarketEntry(None)
        me.token = secrets.token_hex(4)
        me.stamp = arrow.utcnow().timestamp
        me.uid = user.id
        me.uname = user.name
        me.item = item
        me.price = price
        return me

    @property
    def to_dict(self):
        """

        :return:
        :rtype: dict
        """
        return {
            'token': self.token,
            'user_name': self.uname,
            'user_id': self.uid,
            'price': self.price,
            'stamp': self.stamp,
            'item': self.item
        }

    async def save(self, db):
        """

        :param db:
        :type db: sigma.core.mechanics.database.Database
        """
        await db[db.db_nam].MarketEntries.insert_one(self.to_dict)

    @staticmethod
    async def find(db, item=None, token=None):
        """

        :param db:
        :type db: sigma.core.mechanics.database.Database
        :param item:
        :type item: string
        :param token:
        :type token: string
        :return:
        :rtype: MarketEntry
        """
        doc = None
        if item:
            docs = await db[db.db_nam].MarketEntries.find({'item': item}).sort([('price', 1)]).limit(1).to_list(None)
            if docs:
                doc = docs[0]
        if token:
            doc = await db[db.db_nam].MarketEntries.find_one({'token': token})
        entry = None
        if doc:
            entry = MarketEntry(doc)
        return entry

    @staticmethod
    async def find_all_items(db, item, sort=None):
        """

        :param db:
        :type db: sigma.core.mechanics.database.Database
        :param item:
        :type item: tring
        :param sort
        :type sort: dict or tuple
        :return:
        :rtype: list
        """
        entries = []
        curr = db[db.db_nam].MarketEntries.find({'item': item})
        if sort:
            curr.sort([sort])
        docs = await curr.to_list(None)
        for doc in docs:
            entry = MarketEntry(doc)
            entries.append(entry)
        return entries

    @staticmethod
    async def find_all(db, sort=None):
        """

        :param db:
        :type db: sigma.core.mechanics.database.Database
        :param sort:
        :type sort: tuple
        :return:
        :rtype: list
        """
        entries = []
        curr = db[db.db_nam].MarketEntries.find({})
        if sort:
            curr.sort([sort])
        docs = await curr.to_list(None)
        for doc in docs:
            entry = MarketEntry(doc)
            entries.append(entry)
        return entries

    async def delete(self, db):
        """

        :param db:
        :type db: sigma.core.mechanics.database.Database
        """
        await db[db.db_nam].MarketEntries.delete_many(self.to_dict)
