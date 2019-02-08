# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import arrow
from motor import motor_asyncio as motor

from sigma.core.mechanics.config import DatabaseConfig
from sigma.core.mechanics.resources import SigmaResource


class Database(motor.AsyncIOMotorClient):
    def __init__(self, bot, db_cfg: DatabaseConfig):
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

    def get_prefix(self, settings: dict):
        prefix = self.bot.cfg.pref.prefix
        if settings:
            return settings.get('prefix') or prefix
        return prefix

    # Document Pre-Cachers

    async def precache_settings(self):
        self.bot.log.info('Pre-Caching all guild settings...')
        all_settings = await self[self.db_cfg.database].ServerSettings.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('server_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} guild settings.')

    async def precache_profiles(self):
        self.bot.log.info('Pre-Caching all member profiles...')
        all_settings = await self[self.db_cfg.database].Profiles.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('user_id')
            if guild_id:
                await self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} member profiles.')

    async def precache_resources(self):
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

    async def get_guild_settings(self, guild_id: int, setting_name: str = None):
        guild_settings = await self.cache.get_cache(f'settings_{guild_id}')
        if guild_settings is None:
            guild_settings = await self[self.db_nam].ServerSettings.find_one({'server_id': guild_id}) or {}
            await self.cache.set_cache(f'settings_{guild_id}', guild_settings)
        if setting_name:
            return guild_settings.get(setting_name)
        else:
            return guild_settings

    async def set_guild_settings(self, guild_id: int, setting_name: str, value):
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

    async def get_profile(self, user_id: int, entry_name: str = None):
        user_profile = await self[self.db_nam].Profiles.find_one({'user_id': user_id}) or {}
        if entry_name:
            return user_profile.get(entry_name)
        else:
            return user_profile

    async def set_profile(self, user_id: int, entry_name: str, value):
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

    async def is_sabotaged(self, user_id: int):
        return bool(await self.get_profile(user_id, 'sabotaged'))

    # Resource Handling

    async def update_resource(self, user_id: int, resource_name: str, resource: SigmaResource):
        resources = await self[self.db_nam][f'{resource_name.title()}Resource'].find_one({'user_id': user_id})
        coll = self[self.db_nam][f'{resource_name.title()}Resource']
        data = resource.to_dict()
        if resources:
            await coll.update_one({'user_id': user_id}, {'$set': data})
        else:
            data.update({'user_id': user_id})
            await coll.insert_one(data)

    async def get_resource(self, user_id: int, resource_name: str):
        data = await self[self.db_nam][f'{resource_name.title()}Resource'].find_one({'user_id': user_id}) or {}
        resource = SigmaResource(data)
        return resource

    async def add_resource(self, user_id: int, name: str, amount: int, trigger: str, origin=None, ranked: bool = True):
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.add_value(amount, trigger, origin, ranked)
        await self.update_resource(user_id, name, resource)

    async def del_resource(self, user_id: int, name: str, amount: int, trigger: str, origin=None):
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.del_value(amount, trigger, origin)
        await self.update_resource(user_id, name, resource)

    # Inventory Handling

    async def update_inventory(self, user_id: int, inventory: list):
        inv = await self[self.db_nam].Inventory.find_one({'user_id': user_id})
        data = {'items': inventory}
        if inv:
            await self[self.db_nam].Inventory.update_one({'user_id': user_id}, {'$set': data})
        else:
            data.update({'user_id': user_id})
            await self[self.db_nam].Inventory.insert_one(data)

    async def get_inventory(self, user_id: int):
        inventory = await self[self.db_nam].Inventory.find_one({'user_id': user_id}) or {}
        inventory = inventory.get('items', [])
        return inventory

    async def add_to_inventory(self, user_id: int, item_data: dict):
        stamp = arrow.utcnow().timestamp
        item_data.update({'timestamp': stamp})
        inv = await self.get_inventory(user_id)
        inv.append(item_data)
        await self.update_inventory(user_id, inv)

    async def del_from_inventory(self, user_id: int, item_id: str):
        inv = await self.get_inventory(user_id)
        for item in inv:
            if item.get('item_id') == item_id:
                inv.remove(item)
        await self.update_inventory(user_id, inv)

    async def get_inventory_item(self, user_id: int, item_file_id: str):
        inv = await self.get_inventory(user_id)
        output = None
        for item in inv:
            if item.get('item_file_id').lower() == item_file_id.lower():
                output = item
                break
        return output
