import arrow
from motor import motor_asyncio as motor

from sigma.core.mechanics.caching import Cacher


class Database(motor.AsyncIOMotorClient):
    def __init__(self, bot, db_cfg):
        self.bot = bot
        self.db_cfg = db_cfg
        self.cache = Cacher()
        if self.db_cfg.auth:
            self.db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            self.db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            self.db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(self.db_address)

    async def get_guild_settings(self, guild_id, setting_name):
        guild_settings = self.cache.get_cache(guild_id)
        if guild_settings is None:
            guild_settings = await self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
            self.cache.set_cache(guild_id, guild_settings)
        if not guild_settings:
            await self[self.bot.cfg.db.database].ServerSettings.insert_one({'ServerID': guild_id})
            setting_value = None
        else:
            if setting_name in guild_settings:
                setting_value = guild_settings[setting_name]
            else:
                setting_value = None
        return setting_value

    async def set_guild_settings(self, guild_id, setting_name, value):
        self.cache.del_cache(guild_id)
        guild_settings = await self[self.bot.cfg.db.database].ServerSettings.find_one({'ServerID': guild_id})
        if guild_settings:
            update_target = {"ServerID": guild_id}
            update_data = {"$set": {setting_name: value}}
            await self[self.bot.cfg.db.database].ServerSettings.update_one(update_target, update_data)
        else:
            update_data = {'ServerID': guild_id, setting_name: value}
            await self[self.bot.cfg.db.database].ServerSettings.insert_one(update_data)

    async def get_experience(self, user, guild):
        database = self[self.bot.cfg.db.database]
        collection = database['ExperienceSystem']
        entry = await collection.find_one({'UserID': user.id})
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

    async def add_experience(self, user, guild, points, additive=True):
        sabotage_file = await self[self.db_cfg.database].SabotagedUsers.find_one({'UserID': user.id})
        if not sabotage_file:
            database = self[self.bot.cfg.db.database]
            collection = database['ExperienceSystem']
            entry = await collection.find_one({'UserID': user.id})
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
                await collection.insert_one({'UserID': user.id})
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
            await collection.update_one(update_target, update_data)

    async def get_currency(self, user, guild):
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = await collection.find_one({'UserID': user.id})
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

    async def add_currency(self, user, guild, points, additive=True):
        sabotage_file = await self[self.db_cfg.database].SabotagedUsers.find_one({'UserID': user.id})
        if not sabotage_file:
            database = self[self.bot.cfg.db.database]
            collection = database['CurrencySystem']
            entry = await collection.find_one({'UserID': user.id})
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
                await collection.insert_one({'UserID': user.id})
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
            await collection.update_one(update_target, update_data)

    async def rmv_currency(self, user, points):
        database = self[self.bot.cfg.db.database]
        collection = database['CurrencySystem']
        entry = await collection.find_one({'UserID': user.id})
        points = abs(points)
        if entry:
            if 'current' in entry:
                current_amount = entry['current']
            else:
                current_amount = 0
        else:
            await collection.insert_one({'UserID': user.id})
            current_amount = 0
        current_amount -= points
        xp_data = {
            'current': current_amount
        }
        update_target = {'UserID': user.id}
        update_data = {'$set': xp_data}
        await collection.update_one(update_target, update_data)

    async def get_inventory(self, user):
        inventory = await self[self.db_cfg.database]['Inventory'].find_one({'UserID': user.id})
        if not inventory:
            await self[self.db_cfg.database]['Inventory'].insert_one({'UserID': user.id, 'Items': []})
            inventory = []
        else:
            inventory = inventory['Items']
        return inventory

    async def update_inv(self, user, inv):
        await self[self.db_cfg.database]['Inventory'].update_one({'UserID': user.id}, {'$set': {'Items': inv}})

    async def add_to_inventory(self, user, item_data):
        sabotage_file = await self[self.db_cfg.database].SabotagedUsers.find_one({'UserID': user.id})
        if not sabotage_file:
            stamp = arrow.utcnow().timestamp
            item_data.update({'Timestamp': stamp})
            inv = await self.get_inventory(user)
            inv.append(item_data)
            await self.update_inv(user, inv)

    async def del_from_inventory(self, user, item_id):
        inv = await self.get_inventory(user)
        for item in inv:
            if item['item_id'] == item_id:
                inv.remove(item)
        await self.update_inv(user, inv)

    async def get_inventory_item(self, user, item_file_id):
        inv = await self.get_inventory(user)
        output = None
        for item in inv:
            if item['item_file_id'].lower() == item_file_id.lower():
                output = item
                break
        return output
