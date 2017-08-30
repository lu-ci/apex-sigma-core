import pymongo


class Database(pymongo.MongoClient):
    def __init__(self, bot, db_cfg):
        self.bot = bot
        self.db_cfg = db_cfg
        self.settings_cache = {}
        if self.db_cfg.auth:
            db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(db_address)

    def insert_guild_settings(self, guild_id):
        settings_data = {'ServerID': guild_id}
        self[self.bot.cfg.db.database].ServerSettings.insert_one(settings_data)

    def get_guild_settings(self, guild_id, setting_name):
        if guild_id in self.settings_cache:
            guild_settings = self.settings_cache[guild_id]
        else:
            guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
            self.settings_cache.update({guild_id: guild_settings})
        if not guild_settings:
            setting_value = None
            self.insert_guild_settings(guild_id)
        else:
            if setting_name in guild_settings:
                setting_value = guild_settings[setting_name]
            else:
                setting_value = None
        return setting_value

    def set_guild_settings(self, guild_id, setting_name, value):
        if guild_id in self.settings_cache:
            guild_settings = self.settings_cache[guild_id]
            del self.settings_cache[guild_id]
        else:
            guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
        if not guild_settings:
            self.insert_guild_settings(guild_id)
        update_target = {"ServerID": guild_id}
        update_data = {"$set": {setting_name: value}}
        self[self.bot.cfg.db.database].ServerSettings.update_one(update_target, update_data)

    def get_experience(self, user, guild):
        database = self[self.bot.cfg.db.database]
        collection = database['ExperienceSystem']
        entry = collection.find_one({'UserID': user.id})
        if entry:
            global_xp = entry['global']
            guild_id = str(guild.id)
            if guild_id in entry['guilds']:
                guild_xp = entry['guilds'][guild_id]
            else:
                guild_xp = 0
        else:
            global_xp = 0
            guild_xp = 0
        output = {
            'global': global_xp,
            'guild': guild_xp
        }
        return output

    def add_experience(self, user, guild, points):
        database = self[self.bot.cfg.db.database]
        collection = database['ExperienceSystem']
        entry = collection.find_one({'UserID': user.id})
        if entry:
            if 'global' in entry:
                global_xp = entry['global']
            else:
                global_xp = 0
            if 'guilds' in entry:
                guilds = entry['guilds']
            else:
                guilds = {}
        else:
            collection.insert_one({'UserID': user.id})
            global_xp = 0
            guilds = {}
        guild_id = str(guild.id)
        global_xp += points
        if guild_id in guilds:
            guild_points = guilds[guild_id]
        else:
            guild_points = 0
        guild_points += points
        guild_data = {guild_id: guild_points}
        guilds.update(guild_data)
        xp_data = {
            'global': global_xp,
            'guilds': guilds
        }
        update_target = {'UserID': user.id}
        update_data = {'$set': xp_data}
        collection.update_one(update_target, update_data)

    def get_currency(self, user, guild):
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = collection.find_one({'UserID': user.id})
        if entry:
            global_amount = entry['global']
            current_amount = entry['current']
            guild_id = str(guild.id)
            if guild_id in entry['guilds']:
                guild_amount = entry['guilds'][guild_id]
            else:
                guild_amount = 0
        else:
            current_amount = 0
            global_amount = 0
            guild_amount = 0
        output = {
            'current': current_amount,
            'global': global_amount,
            'guild': guild_amount
        }
        return output

    def add_currency(self, user, guild, points):
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = collection.find_one({'UserID': user.id})
        points = abs(points)
        if entry:
            if 'current' in entry:
                current_amount = entry['current']
            else:
                current_amount = 0
            if 'global' in entry:
                global_amount = entry['global']
            else:
                global_amount = 0
            if 'guilds' in entry:
                guilds = entry['guilds']
            else:
                guilds = {}
        else:
            collection.insert_one({'UserID': user.id})
            global_amount = 0
            current_amount = 0
            guilds = {}
        guild_id = str(guild.id)
        global_amount += points
        if guild_id in guilds:
            guild_points = guilds[guild_id]
        else:
            guild_points = 0
        current_amount += points
        guild_points += points
        guild_data = {guild_id: guild_points}
        guilds.update(guild_data)
        xp_data = {
            'current': current_amount,
            'global': global_amount,
            'guilds': guilds
        }
        update_target = {'UserID': user.id}
        update_data = {'$set': xp_data}
        collection.update_one(update_target, update_data)

    def rmv_currency(self, user, points):
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = collection.find_one({'UserID': user.id})
        points = abs(points)
        if entry:
            if 'current' in entry:
                current_amount = entry['current']
            else:
                current_amount = 0
        else:
            collection.insert_one({'UserID': user.id})
            current_amount = 0
        current_amount -= points
        xp_data = {
            'current': current_amount
        }
        update_target = {'UserID': user.id}
        update_data = {'$set': xp_data}
        collection.update_one(update_target, update_data)

    def get_inventory(self, user):
        inventory = self[self.db_cfg.database]['Inventory'].find_one({'UserID': user.id})
        if not inventory:
            self[self.db_cfg.database]['Inventory'].insert_one({'UserID': user.id, 'Items': []})
            inventory = []
        else:
            inventory = inventory['Items']
        return inventory

    def update_inv(self, user, inv):
        self[self.db_cfg.database]['Inventory'].update_one(
            {'UserID': user.id},
            {
                '$set': {'Items': inv}
            }
        )

    def add_to_inventory(self, user, item_data):
        inv = self.get_inventory(user)
        inv.append(item_data)
        self.update_inv(user, inv)

    def del_from_inventory(self, user, item_id):
        inv = self.get_inventory(user)
        for item in inv:
            if item['item_id'] == item_id:
                inv.remove(item)
        self.update_inv(user, inv)

    def get_inventory_item(self, user, item_file_id):
        inv = self.get_inventory(user)
        output = None
        for item in inv:
            if item['item_file_id'].lower() == item_file_id.lower():
                output = item
                break
        return output
