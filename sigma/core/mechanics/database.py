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
