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
        :type bot: sigma.core.sigma.ApexSigma
        :type db_cfg: sigma.core.mechanics.config.DatabaseConfig
        """
        self.bot = bot
        self.db_cfg = db_cfg
        self.cache = self.bot.cache
        if self.db_cfg.auth:
            self.db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            self.db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            self.db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(self.db_address)

    @property
    def col(self):
        """
        Makes for a shorter syntax when accessing collections.
        Somewhat deceptive as this just returns the database.
        """
        return self[self.db_cfg.database]

    def get_prefix(self, settings):
        """
        Gets the prefix from a command payload.
        :type settings: dict
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
        """
        self.bot.log.info('Pre-Caching all guild settings...')
        all_settings = await self.col.ServerSettings.find().to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('server_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} guild settings.')

    async def precache_profiles(self):
        """
        Caches all user profile for all guilds on startup
        to reduce database load during regular functionality.
        """
        self.bot.log.info('Pre-Caching all member profiles...')
        all_settings = await self.col.Profiles.find().to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('user_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} member profiles.')

    async def precache_resources(self):
        """
        Caches all user resources for all guilds on startup
        to reduce database load during regular functionality.
        """
        self.bot.log.info('Pre-Caching all resource data...')
        res_cache_counter = 0
        all_colls = await self[self.db_cfg.database].list_collection_names()
        for coll in all_colls:
            if coll.endswith('Resource'):
                res_nam = coll[:8].lower()
                docs = await self.col[coll].find().to_list(None)
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
        :type guild_id: int
        :type setting_name: str
        :rtype: bool or int or float or str or list or dict
        """
        guild_settings = await self.cache.get_cache(f'settings_{guild_id}')
        if guild_settings is None:
            guild_settings = await self.col.ServerSettings.find_one({'server_id': guild_id}) or {}
            await self.cache.set_cache(f'settings_{guild_id}', guild_settings)
        if setting_name:
            return guild_settings.get(setting_name)
        else:
            return guild_settings

    async def set_guild_settings(self, guild_id, setting_name, value):
        """
        Sets a settings entry for the given Guild ID.
        :type guild_id: int
        :type setting_name: str or int
        :type value: bool or int or float or str or list or dict
        """
        guild_settings = await self.col.ServerSettings.find_one({'server_id': guild_id})
        if guild_settings is None:
            guild_settings = {'server_id': guild_id}
        set_data = {setting_name: value}
        guild_settings.update(set_data)
        await self.col.ServerSettings.update_one({"server_id": guild_id}, {"$set": set_data}, upsert=True)
        await self.cache.set_cache(f'settings_{guild_id}', guild_settings)

    # Profile Data Entry Variable Calls

    async def get_profile(self, user_id, entry_name=None):
        """
        Gets the profile document for the given User ID.
        :type user_id: int
        :type entry_name: str
        :rtype: bool or int or float or str or list or dict
        """
        user_profile = await self.col.Profiles.find_one({'user_id': user_id}) or {}
        if entry_name:
            return user_profile.get(entry_name)
        else:
            return user_profile

    async def set_profile(self, user_id, entry_name, value):
        """
        Sets a user's profile value for the given key.
        :type user_id: int
        :type entry_name: str
        :type value: bool or int or float or str or list or dict
        """
        user_profile = await self.col.Profiles.find_one({'user_id': user_id}) or {}
        set_data = {entry_name: value}
        user_profile.update(set_data)
        await self.col.Profiles.update_one({"user_id": user_id}, {"$set": set_data}, upsert=True)

    async def is_sabotaged(self, user_id):
        """
        Returns if the user is sabotaged/quarantined or not.
        :type user_id: int
        :rtype: bool
        """
        sabotaged = bool(await self.get_profile(user_id, 'sabotaged'))
        if not sabotaged:
            lookup = {'user_id': user_id, 'total': True}
            sabotaged = bool(await self.db.col.BlacklistedUsers.count_documents(lookup))
        return sabotaged

    # Resource Handling

    async def update_resource(self, user_id, resource_name, resource):
        """
        Updates a user's resource document in the database.
        :type user_id: int
        :type resource_name: str
        :type resource: sigma.core.mechanics.resources.SigmaResource
        """
        await self.col[f'{resource_name.title()}Resource'].update_one(
            {'user_id': user_id}, {'$set': resource.to_dict()}, upsert=True)

    async def get_resource(self, user_id, resource_name):
        """
        Returns a resource class for the given user id and resource name.
        :type user_id: int
        :type resource_name: str
        :rtype: sigma.core.mechanics.resources.SigmaResource
        """
        data = await self.col[f'{resource_name.title()}Resource'].find_one({'user_id': user_id}) or {}
        resource = SigmaResource(data)
        return resource

    async def add_resource(self, user_id, name, amount, trigger, origin=None, ranked=True):
        """
        Increases a user's resource by type.
        :type user_id: int
        :type name: str
        :type amount: int
        :type trigger: str
        :type origin: discord.Message or None
        :type ranked: bool
        """
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.add_value(amount, trigger, origin, ranked)
        await self.update_resource(user_id, name, resource)

    async def del_resource(self, user_id, name, amount, trigger, origin=None):
        """
        Decreases a user's resource by type.
        :type user_id: int
        :type name: str
        :type amount: int
        :type trigger: str
        :type origin: discord.Message
        """
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.del_value(amount, trigger, origin)
        await self.update_resource(user_id, name, resource)

    # Inventory Handling

    async def update_inventory(self, user_id, inventory):
        """
        Updates the user's inventory database document.
        :type user_id: int
        :type inventory: list
        """
        await self.col.Inventory.update_one(
            {'user_id': user_id}, {'$set': {'items': inventory}}, upsert=True)

    async def get_inventory(self, user_id):
        """
        Gets a user's inventory item list.
        :type user_id: int
        :rtype: list
        """
        inventory = await self.col.Inventory.find_one({'user_id': user_id}) or {}
        inventory = inventory.get('items', [])
        return inventory

    async def add_to_inventory(self, user_id, item_data):
        """
        Adds a new entry to a user's inventory.
        :type user_id: int
        :type item_data: dict
        """
        stamp = arrow.utcnow().int_timestamp
        item_data.update({'timestamp': stamp})
        inv = await self.get_inventory(user_id)
        inv.append(item_data)
        await self.update_inventory(user_id, inv)

    async def del_from_inventory(self, user_id, item_id):
        """
        Removes an item from the user's inventory.
        :type user_id: int
        :type item_id: str
        """
        inv = await self.get_inventory(user_id)
        for item in inv:
            if item.get('item_id') == item_id:
                inv.remove(item)
        await self.update_inventory(user_id, inv)

    async def get_inventory_item(self, user_id, item_file_id):
        """
        Get one specific item from the user's inventory.
        :type user_id: int
        :type item_file_id: str
        :rtype: dict
        """
        inv = await self.get_inventory(user_id)
        output = None
        for item in inv:
            if item.get('item_file_id').lower() == item_file_id.lower():
                output = item
                break
        return output
