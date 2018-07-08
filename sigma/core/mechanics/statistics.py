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

import asyncio

from sigma.core.mechanics.database import Database


class StatisticsStorage(object):
    def __init__(self, db: Database, name: str):
        self.db = db
        self.loop = asyncio.get_event_loop()
        self.name = name
        self.count = 0
        self.loop.create_task(self.insert_stats())

    def add_stat(self):
        self.count += 1

    async def insert_stats(self):
        while True:
            def_stat_data = {'event': self.name, 'count': 0}
            collection = 'EventStats'
            database = self.db.db_nam
            check = await self.db[database][collection].find_one({"event": self.name})
            if not check:
                await self.db[database][collection].insert_one(def_stat_data)
                ev_count = 0
            else:
                ev_count = check.get('count', 0)
            ev_count += self.count
            update_target = {"event": self.name}
            update_data = {"$set": {'count': ev_count}}
            await self.db[database][collection].update_one(update_target, update_data)
            self.count = 0
            await asyncio.sleep(60)
