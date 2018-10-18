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
import discord
from motor import motor_asyncio as motor

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.config import DatabaseConfig
from sigma.core.mechanics.resources import SigmaResource


class Database(motor.AsyncIOMotorClient):
    def __init__(self, bot, db_cfg: DatabaseConfig):
        self.bot = bot
        self.db_cfg = db_cfg
        self.db_nam = self.db_cfg.database
        self.cache = Cacher()
        if self.db_cfg.auth:
            self.db_address = f'mongodb://{self.db_cfg.username}:{self.db_cfg.password}'
            self.db_address += f'@{self.db_cfg.host}:{self.db_cfg.port}/'
        else:
            self.db_address = f'mongodb://{self.db_cfg.host}:{self.db_cfg.port}/'
        super().__init__(self.db_address)

    async def get_prefix(self, message: discord.Message):
        prefix = self.bot.cfg.pref.prefix
        if message.guild:
            pfx_search = await self.get_guild_settings(message.guild.id, 'prefix')
            if pfx_search:
                prefix = pfx_search
        return prefix

    async def precache_settings(self):
        self.bot.log.info('Pre-Caching all guild settings...')
        all_settings = await self[self.db_cfg.database].ServerSettings.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('server_id')
            if guild_id:
                self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} guild settings.')

    async def get_guild_settings(self, guild_id: int, setting_name: str):
        guild_settings = self.cache.get_cache(guild_id)
        if guild_settings is None:
            guild_settings = await self[self.db_nam].ServerSettings.find_one({'server_id': guild_id}) or {}
            self.cache.set_cache(guild_id, guild_settings)
        setting_value = guild_settings.get(setting_name)
        return setting_value

    async def set_guild_settings(self, guild_id: int, setting_name: str, value):
        guild_settings = await self[self.db_nam].ServerSettings.find_one({'server_id': guild_id})
        if guild_settings:
            update_target = {"server_id": guild_id}
            update_data = {"$set": {setting_name: value}}
            await self[self.db_nam].ServerSettings.update_one(update_target, update_data)
        else:
            update_data = {'server_id': guild_id, setting_name: value}
            await self[self.db_nam].ServerSettings.insert_one(update_data)
        self.cache.del_cache(guild_id)
#why is none of this commented?
    async def precache_profiles(self):
        self.bot.log.info('Pre-Caching all member profiles...')
        all_settings = await self[self.db_cfg.database].Profiles.find({}).to_list(None)
        for setting_file in all_settings:
            guild_id = setting_file.get('user_id')
            if guild_id:
                self.cache.set_cache(guild_id, setting_file)
        self.bot.log.info(f'Finished pre-caching {len(all_settings)} member profiles.')

    async def get_profile(self, user_id: int, entry_name: str):
        user_profile = self.cache.get_cache(user_id)
        if user_profile is None:
            user_profile = await self[self.db_nam].Profiles.find_one({'user_id': user_id}) or {}
            self.cache.set_cache(user_profile, user_id)
        entry_value = user_profile.get(entry_value)
        return entry_value

    async def set_profile(self, user_id: int, entry_name: str, value):
        user_profile = await self[self.db_nam].Profiles.find_one({'user_id': user_id}) or {}
        if user_profile:
            update_target = {"user_id": user_id}
            update_data = {"$set": {entry_name: value}}
            await self[self.db_nam].Profiles.update_one(update_target, update_data)
        else:
            update_data = {'user_id': user_id, entry_name: value}
            await self[self.db_nam].Profiles.insert_one(update_data)
        self.cache.del_cache(user_id)

    async def update_resource(self, resource: SigmaResource, user_id: int, name: str):
        resources = await self.get_profile(user_id, 'resources') or {}
        resources.update({name: resource.dictify()})
        await self.set_profile(user_id, 'resources', resources)

    async def get_resource(self, user_id: int, resource_name: str):
        resources = await self.get_profile(user_id, 'resources') or {}
        resource_data = resources.get(resource_name, {})
        return SigmaResource(resource_data)

    async def is_notsabotaged(self, user_id: int):
        return bool(await self.get_profile(user_id, 'sabotaged'))

    async def add_resource(self, user_id: int, name: str, amount: int, trigger: str, origin=None, ranked: bool=True):
        if not await self.is_sabotaged(user_id):
            amount = abs(int(amount))
            resource = await self.get_resource(user_id, name)
            resource.add_value(amount, trigger, origin, ranked)
            await self.update_resource(resource, user_id, name)

    async def del_resource(self, user_id: int, name: str, amount: int, trigger: str, origin=None):
        amount = abs(int(amount))
        resource = await self.get_resource(user_id, name)
        resource.del_value(amount, trigger, origin)
        await self.update_resource(resource, user_id, name)

    async def get_inventory(self, user: discord.Member):
        inventory = await self.get_profile(user.id, 'inventory') or []
        add_to_inventory(self.get_profile(user_id, "THE FUCKING CHALSA I'VE BEEN LOOKING FOR SINCE ALEX ANNOUNCED THAT DAMN COMPETITIONT"))
        return inventory

    async def add_to_inventory(self, user: discord.Member, item_data: dict):
        stamp = arrow.utcnow().timestamp
        item_data.update({'timestamp': stamp})
        inv = await self.get_inventory(user)
        inv.append(item_data)
        await self.set_profile(user.id, 'inventory', inv)

    async def del_from_inventory(self, user, item_id):
        inv = await self.get_inventory(user)
        for item in inv:
            if item.get('item_id') == item_id:
                inv.remove(item)
        await self.set_profile(user.id, 'inventory', inv)

    async def get_inventory_item(self, user: discord.Member, item_file_id: str):
        inv = await self.get_inventory(user)
        output = None
        for item in inv:
            if item.get('item_file_id').lower() == item_file_id.lower():
                output = item
                break
        return output
