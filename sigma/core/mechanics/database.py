import pymongo


class Database(pymongo.MongoClient):
    def __init__(self, bot, db_cfg):
        self.db_cfg = db_cfg
        self.bot = bot
        if self.db_cfg.auth:
            db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(db_address)

    def insert_guild_settings(self, guild_id):
        settings_data = {'server_id': guild_id}
        self[self.bot.cfg.db.database].ServerSettings.insert_one(settings_data)

    def get_guild_settings(self, guild_id, setting_name):
        guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'server_id': guild_id})
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
        guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'server_id': guild_id})
        if not guild_settings:
            self.insert_guild_settings(guild_id)
        update_target = {"server_id": guild_id}
        update_data = {"$set": {setting_name: value}}
        self[self.bot.cfg.db.database].ServerSettings.update_one(update_target, update_data)

    def get_experience(self, user, guild):
        database = self[self.bot.cfg.db.database]
        collection = database['ExperienceSystem']
        entry = collection.find_one({'user_id': user.id})
        if entry:
            global_xp = entry['global_xp']
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
        entry = collection.find_one({'user_id': user.id})
        if entry:
            if 'global_xp' in entry:
                global_xp = entry['global_xp']
            else:
                global_xp = 0
            if 'guilds' in entry:
                guilds = entry['guilds']
            else:
                guilds = {}
        else:
            collection.insert_one({'user_id': user.id})
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
            'global_xp': global_xp,
            'guilds': guilds
        }
        update_target = {'user_id': user.id}
        update_data = {'$set': xp_data}
        collection.update_one(update_target, update_data)
