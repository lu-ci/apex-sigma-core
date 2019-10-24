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

import arrow
from motor import motor_asyncio as motor

from sigma.core.mechanics.resources import SigmaResource


class Database(motor.AsyncIOMotorClient):
    """
    Sigma's core database handler and function abstraction center.
    Handles all communication with a MongoDB server instance.
    """

    def __init__(self, bot, db_cfg):
        """
        :param bot: The main client core reference.
        :type bot: sigma.core.sigma.ApexSigma
        :param db_cfg: The database configuration class.
        :type db_cfg: sigma.core.mechanics.config.DatabaseConfig
        """
        self.bot = bot
        self.db_cfg = db_cfg
        self.db_nam = self.db_cfg.database
        self.cache = self.bot.cache
        if self.db_cfg.auth:
            self.db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            self.db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            self.db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(self.db_address)

    def get_prefix(self, settings):
        """
        Gets the prefix from a command payload.
        :param settings: The payload settings of the guild.
        :type settings: dict
        :return:
        :rtype: str
        """
        prefix = self.bot.cfg.pref.prefix
        if settings:
            return settings.get('prefix') or prefix
        return prefix

    # Document Pre-Cachers

    async def precache_settings(self):
        """
        Caches all settings files for all guilds on startup
        to reduce database load during regular functionality.
        :return:
        :rtype:
        """
        self.bot.log.info('Pre-Caching all guild settings...')
        all_settings = await self[self.db_cfg.database].ServerSettings.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('server_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} guild settings.')

    async def precache_profiles(self):
        """
        Caches all user profile for all guilds on startup
        to reduce database load during regular functionality.
        :return:
        :rtype:
        """
        self.bot.log.info('Pre-Caching all member profiles...')
        all_settings = await self[self.db_cfg.database].Profiles.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('user_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} member profiles.')

    async def precache_resources(self):
        """
        Caches all user resources for all guilds on startup
        to reduce database load during regular functionality.
        :return:
        :rtype:
        """
        self.bot.log.info('Pre-Caching all resource data...')
        res_cache_counter = 0
        all_colls = await self[self.db_nam].list_collection_names()
        for coll in all_colls:
            if coll.endswith('Resource'):
                res_nam = coll[:8].lower()
                docs = await self[self.db_nam][coll].find({}).to_list(None)
                for doc in docs:
                    uid = doc.get('user_id')
                    cache_key = f'res_{res_nam}_{uid}'
                    resource = SigmaResource(doc)
                    await self.cache.set_cache(cache_key, resource)
                    res_cache_counter += 1
        self.bot.log.info(f'Finished pre-caching {res_cache_counter} resource entries.')

    # Guild Setting Variable Calls

    async def get_guild_settings(self, guild_id, setting_name=None):
        """
        Gets the settings document for a specified Guild ID
        or a specific setting value for a given settings key.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param setting_name: Requested settings value key.
        :type setting_name: str
        :return:
        :rtype: bool or int or float or str or list or dict
        """
        guild_settings = await self.cache.get_cache(f'settings_{guild_id}')
        if guild_settings is None:
            guild_settings = await self[self.db_nam].ServerSettings.find_one({'server_id': guild_id}) or {}
            await self.cache.set_cache(f'settings_{guild_id}', guild_settings)
        if setting_name:
            return guild_settings.get(setting_name)
        else:
            return guild_settings

    async def set_guild_settings(self, guild_id, setting_name, value):
        """
        Sets a settings entry for the given Guild ID.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param setting_name: The settings value key.
        :type setting_name: str or int
        :param value: The settings value.
        :type value: bool or int or float or str or list or dict
        :return:
        :rtype:
        """
        guild_settings = await self[self.db_nam].ServerSettings.find_one({'server_id': guild_id})
        if guild_settings:
            update_target = {"server_id": guild_id}
            set_data = {setting_name: value}
            update_data = {"$set": set_data}
            guild_settings.update(set_data)
            await self[self.db_nam].ServerSettings.update_one(update_target, update_data)
        else:
            guild_settings = {'server_id': guild_id, setting_name: value}
            await self[self.db_nam].ServerSettings.insert_one(guild_settings)
        await self.cache.set_cache(f'settings_{guild_id}', guild_settings)

    # Profile Data Entry Variable Calls

    async def get_profile(self, user_id, entry_name=None):
        """
        Gets the profile document for the given User ID.
        :param user_id: The User ID.
        :type user_id: int
        :param entry_name: The key for the profile value entry.
        :type entry_name: str
        :return:
        :rtype: bool or int or float or str or list or dict
        """
        user_profile = await self[self.db_nam].Profiles.find_one({'user_id': user_id}) or {}
        if entry_name:
            return user_profile.get(entry_name)
        else:
            return user_profile

    async def set_profile(self, user_id, entry_name, value):
        """
        Sets a user's profile value for the given key.
        :param user_id: The User ID.
        :type user_id: int
        :param entry_name: The key for the profile value.
        :type entry_name: str
        :param value: The value of the entry.
        :type value: bool or int or float or str or list or dict
        :return:
        :rtype:
        """
        user_profile = await self[self.db_nam].Profiles.find_one({'user_id': user_id}) or {}
        if user_profile:
            update_target = {"user_id": user_id}
            set_data = {entry_name: value}
            update_data = {"$set": set_data}
            user_profile.update(set_data)
            await self[self.db_nam].Profiles.update_one(update_target, update_data)
        else:
            user_profile = {'user_id': user_id, entry_name: value}
            await self[self.db_nam].Profiles.insert_one(user_profile)

    async def is_sabotaged(self, user_id):
        """
        Returns if the user is sabotaged/quarantined or not.
        :param user_id: The User ID.
        :type user_id: int
        :return:
        :rtype: bool
        """
        sabbed = bool(await self.get_profile(user_id, 'sabotaged'))
        if not sabbed:
            coll = self.db[self.db_nam].BlacklistedUsers
            lookup = {'user_id': user_id, 'total': True}
            sabbed = bool(await coll.count_documents(lookup))
        return sabbed

    # Resource Handling

    async def update_resource(self, user_id, resource_name, resource):
        """
        Updates a user's resource document in the database.
        :param user_id: The User ID.
        :type user_id: int
        :param resource_name: The name of the resource.
        :type resource_name: str
        :param resource: The resource abstraction class.
        :type resource: sigma.core.mechanics.resources.SigmaResource
        :return:
        :rtype:
        """
        resources = await self[self.db_nam][f'{resource_name.title()}Resource'].find_one({'user_id': user_id})
        coll = self[self.db_nam][f'{resource_name.title()}Resource']
        data = resource.to_dict()
        if resources:
            await coll.update_one({'user_id': user_id}, {'$set': data})
        else:
            data.update({'user_id': user_id})
            await coll.insert_one(data)

    async def get_resource(self, user_id, resource_name):
        """
        Returns a resource class for the given user id and resource name.
        :param user_id: The User ID.
        :type user_id: int
        :param resource_name: The name of the resource.
        :type resource_name: str
        :return:
        :rtype: sigma.core.mechanics.resources.SigmaResource
        """
        data = await self[self.db_nam][f'{resource_name.title()}Resource'].find_one({'user_id': user_id}) or {}
        resource = SigmaResource(data)
        return resource

    async def add_resource(self, user_id, name, amount, trigger, origin=None, ranked=True):
        """
        Increases a user's resource by type.
        :param user_id: The User ID.
        :type user_id: int
        :param name: The name of the resource.
        :type name: str
        :param amount: Amount to modify the value by.
        :type amount: int
        :param trigger: The function that caused the change.
        :type trigger: str
        :param origin: The origin of the change.
        :type origin: discord.Message or None
        :param ranked: If this change counts towards the leaderboard.
        :type ranked: bool
        :return:
        :rtype:
        """
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.add_value(amount, trigger, origin, ranked)
        await self.update_resource(user_id, name, resource)

    async def del_resource(self, user_id, name, amount, trigger, origin=None):
        """
        Decreases a user's resource by type.
        :param user_id: The User ID.
        :type user_id: int
        :param name: The name of the resource.
        :type name: str
        :param amount: Amount to modify the value by.
        :type amount: int
        :param trigger: The function that caused the change.
        :type trigger: str
        :param origin: The origin of the change.
        :type origin: discord.Message
        :return:
        :rtype:
        """
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.del_value(amount, trigger, origin)
        await self.update_resource(user_id, name, resource)

    # Inventory Handling

    async def update_inventory(self, user_id, inventory):
        """
        Updates the user's inventory database document.
        :param user_id: The User ID.
        :type user_id: int
        :param inventory: The list of all their inventory items.
        :type inventory: list[dict]
        :return:
        :rtype:
        """
        inv = await self[self.db_nam].Inventory.find_one({'user_id': user_id})
        data = {'items': inventory}
        if inv:
            await self[self.db_nam].Inventory.update_one({'user_id': user_id}, {'$set': data})
        else:
            data.update({'user_id': user_id})
            await self[self.db_nam].Inventory.insert_one(data)

    async def get_inventory(self, user_id):
        """
        Gets a usre's inventory item list.
        :param user_id: The User ID.
        :type user_id: int
        :return:
        :rtype: list[dict]
        """
        inventory = await self[self.db_nam].Inventory.find_one({'user_id': user_id}) or {}
        inventory = inventory.get('items', [])
        return inventory

    async def add_to_inventory(self, user_id, item_data):
        """
        Adds a new entry to a user's inventory.
        :param user_id: The User ID.
        :type user_id: int
        :param item_data: The item entry data.
        :type item_data: dict
        :return:
        :rtype:
        """
        stamp = arrow.utcnow().timestamp
        item_data.update({'timestamp': stamp})
        inv = await self.get_inventory(user_id)
        inv.append(item_data)
        await self.update_inventory(user_id, inv)

    async def del_from_inventory(self, user_id, item_id):
        """
        Removes an item from the user's inventory.
        :param user_id: The User ID.
        :type user_id: int
        :param item_id: The item's ID.
        :type item_id: str
        :return:
        :rtype:
        """
        inv = await self.get_inventory(user_id)
        for item in inv:
            if item.get('item_id') == item_id:
                inv.remove(item)
        await self.update_inventory(user_id, inv)

    async def get_inventory_item(self, user_id, item_file_id):
        """
        Get one specific item from the user's inventory.
        :param user_id: The User ID.
        :type user_id: int
        :param item_file_id: The item's ID.
        :type item_file_id: str
        :return:
        :rtype: dict
        """
        inv = await self.get_inventory(user_id)
        output = None
        for item in inv:
            if item.get('item_file_id').lower() == item_file_id.lower():
                output = item
                break
        return output
