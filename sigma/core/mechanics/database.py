import arrow
import pymongo


class Database(pymongo.MongoClient):
    """
    Database class contained that uses the pymongo.MongoClient
    as it's base for all functions. Requires a running MongoDB
    server to connect to. Includes methods that simplify some
    more complex operations, like statistics and inventories.
    :param bot:
    :param db_cfg:
    """

    def __init__(self, bot, db_cfg):
        self.bot = bot
        self.db_cfg = db_cfg
        if self.db_cfg.auth:
            self.db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            self.db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            self.db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(self.db_address)

    def insert_guild_settings(self, guild_id):
        """
        If no guild settings exist,
        this method creates a new blank settings file
        for the guild in the database.
        :param guild_id:
        :return:
        """
        settings_data = {'ServerID': guild_id}
        self[self.bot.cfg.db.database].ServerSettings.insert_one(settings_data)

    def get_guild_settings(self, guild_id, setting_name):
        """
        Retrieves the setting by the inputted setting name
        for the inputted guild id. If the setting is not set
        it will return None as it's result.
        :param guild_id:
        :param setting_name:
        :return:
        """
        guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
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
        """
        Writes to the guild's settings file.
        Sets the specified setting name to the specified value.
        :param guild_id:
        :param setting_name:
        :param value:
        :return:
        """
        guild_settings = self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
        if not guild_settings:
            self.insert_guild_settings(guild_id)
        update_target = {"ServerID": guild_id}
        update_data = {"$set": {setting_name: value}}
        self[self.bot.cfg.db.database].ServerSettings.update_one(update_target, update_data)

    def get_experience(self, user, guild):
        """
        Get's a user's experience points.
        :param user:
        :param guild:
        :return:
        """
        database = self[self.bot.cfg.db.database]
        collection = database['ExperienceSystem']
        entry = collection.find_one({'UserID': user.id})
        if entry:
            if 'global' in entry:
                global_xp = entry['global']
            else:
                global_xp = 0
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

    def add_experience(self, user, guild, points, additive=True):
        """
        Adds experience points to a user.
        :param user:
        :param guild:
        :param points:
        :param additive:
        :return:
        """
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
        if guild_id in guilds:
            guild_points = guilds[guild_id]
        else:
            guild_points = 0
        if additive:
            global_xp += points
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
        """
        Gets a user's current currency value.
        :param user:
        :param guild:
        :return:
        """
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = collection.find_one({'UserID': user.id})
        if entry:
            if 'global' in entry:
                global_amount = entry['global']
            else:
                global_amount = 0
            current_amount = entry['current']
            guild_id = str(guild.id)
            if 'guilds' in entry:
                if guild_id in entry['guilds']:
                    guild_amount = entry['guilds'][guild_id]
                else:
                    guild_amount = 0
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

    def add_currency(self, user, guild, points, additive=True):
        """
        Adds to the user's currency value.
        :param user:
        :param guild:
        :param points:
        :param additive:
        :return:
        """
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
        if guild_id in guilds:
            guild_points = guilds[guild_id]
        else:
            guild_points = 0
        if additive:
            global_amount += points
            guild_points += points
        current_amount += points
        guild_data = {guild_id: guild_points}
        guilds.update(guild_data)
        xp_data = {
            'current': current_amount,
            'global': int(global_amount),
            'guilds': guilds
        }
        update_target = {'UserID': user.id}
        update_data = {'$set': xp_data}
        collection.update_one(update_target, update_data)

    def rmv_currency(self, user, points):
        """
        Subtracts a user's currency.
        :param user:
        :param points:
        :return:
        """
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
        """
        Get's a user's inventory.
        :param user:
        :return:
        """
        inventory = self[self.db_cfg.database]['Inventory'].find_one({'UserID': user.id})
        if not inventory:
            self[self.db_cfg.database]['Inventory'].insert_one({'UserID': user.id, 'Items': []})
            inventory = []
        else:
            inventory = inventory['Items']
        return inventory

    def update_inv(self, user, inv):
        """
        Update's a user's inventory with the new input.
        :param user:
        :param inv:
        :return:
        """
        self[self.db_cfg.database]['Inventory'].update_one(
            {'UserID': user.id},
            {
                '$set': {'Items': inv}
            }
        )

    def add_to_inventory(self, user, item_data):
        """
        Adds an item to the ite's inventory.
        :param user:
        :param item_data:
        :return:
        """
        stamp = arrow.utcnow().timestamp
        item_data.update({'Timestamp': stamp})
        inv = self.get_inventory(user)
        inv.append(item_data)
        self.update_inv(user, inv)

    def del_from_inventory(self, user, item_id):
        """
        Removes an item from the users inventory.
        :param user:
        :param item_id:
        :return:
        """
        inv = self.get_inventory(user)
        for item in inv:
            if item['item_id'] == item_id:
                inv.remove(item)
        self.update_inv(user, inv)

    def get_inventory_item(self, user, item_file_id):
        """
        Get a specific item from the user's inventory.
        :param user:
        :param item_file_id:
        :return:
        """
        inv = self.get_inventory(user)
        output = None
        for item in inv:
            if item['item_file_id'].lower() == item_file_id.lower():
                output = item
                break
        return output
