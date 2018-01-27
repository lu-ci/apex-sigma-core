import asyncio
import json

import aiohttp


class ElasticHandler(object):
    def __init__(self, url, index):
        self.url = url
        self.type = index

    async def post(self, data):
        qry = json.dumps(data)
        api_url = f'{self.url}/{self.type}/doc/'
        heads = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(api_url, data=qry, headers=heads)
        except Exception:
            pass


class StatisticsStorage(object):
    def __init__(self, db, name):
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
            database = self.db.db_cfg.database
            check = await self.db[database][collection].find_one({"event": self.name})
            if not check:
                await self.db[database][collection].insert_one(def_stat_data)
                ev_count = 0
            else:
                ev_count = check['count']
            ev_count += self.count
            update_target = {"event": self.name}
            update_data = {"$set": {'count': ev_count}}
            await self.db[database][collection].update_one(update_target, update_data)
            self.count = 0
            await asyncio.sleep(60)
