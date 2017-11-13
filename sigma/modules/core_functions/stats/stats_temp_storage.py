import asyncio


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
            check = self.db[database][collection].find_one({"event": self.name})
            if not check:
                self.db[database][collection].insert_one(def_stat_data)
                ev_count = 0
            else:
                ev_count = check['count']
            ev_count += self.count
            update_target = {"event": self.name}
            update_data = {"$set": {'count': ev_count}}
            self.db[database][collection].update_one(update_target, update_data)
            self.count = 0
            await asyncio.sleep(60)
