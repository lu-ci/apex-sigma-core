from fuzzywuzzy import fuzz, process

from .scrapper_core import FEHScrapper


class FireEmblemHeroesCore(object):
    def __init__(self, db):
        self.db = db
        self.data_dir = 'sigma/modules/games/fireemblemheroes/mech/data'
        self.scrapper = FEHScrapper(self)
        self.colors = self.scrapper.get_yaml_data(self.data_dir + '/colors.yml')
        self.move_icons = self.scrapper.get_yaml_data(self.data_dir + '/move_icons.yml')
        self.weapon_icons = self.scrapper.get_yaml_data(self.data_dir + '/weapon_icons.yml')
        self.index = {}

    async def feh_dbcheck(self):
        item_count = await self.db[self.db.db_cfg.database].FEHData.count()
        if not item_count:
            scrapped_data = await self.scrapper.scrap_all()
            await self.insert_into_db(scrapped_data)

    async def insert_into_db(self, data):
        all_data = []
        for items in data:
            for item_id in items:
                all_data.append(items[item_id])
        if all_data:
            await self.db[self.db.db_cfg.database].FEHData.insert_many(all_data)

    async def init_index(self):
        all_data = await self.db[self.db.db_cfg.database].FEHData.find().to_list(None)
        for record in all_data:
            self.index[record['id']] = record['id']
            try:
                for alias in record['alias']:
                    self.index[alias] = record['id']
            except KeyError:
                pass

    async def lookup(self, query):
        matches = process.extract(query, self.index.keys(), scorer=fuzz.ratio)
        result = None
        # Workaround for fuzzywuzzy stripping + and inability to access + variants of weapons because of that
        if query[-1] == '+':
            for match in matches:
                if match[0].find('+') != -1:
                    result = match[0]
                    break
        else:
            result = matches[0][0]
        if result:
            result = await self.db[self.db.db_cfg.database].FEHData.find_one({'id': self.index[result]})
        return result

    @staticmethod
    def get_specified_rarity(query):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for key_index, key_char in enumerate(query):
            if key_char in numbers:
                return int(key_char)
