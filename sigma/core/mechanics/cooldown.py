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

from sigma.core.mechanics.caching import Cacher


class CommandRateLimiter(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.stamps = {}

    def is_cooling(self, message):
        timeout = 1.25
        last_stamp = self.stamps.get(message.author.id, 0)
        curr_stamp = arrow.utcnow().float_timestamp
        return (last_stamp + timeout) > curr_stamp

    def set_cooling(self, message):
        if message.author.id not in self.cmd.bot.cfg.dsc.owners:
            self.stamps.update({message.author.id: arrow.utcnow().float_timestamp})


class CooldownControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        self.cache = Cacher()
        self.cds = self.db[self.db.db_nam].CooldownSystem

    async def cache_cooldowns(self):
        cooldowns = await self.cds.find({}).to_list(None)
        for cooldown in cooldowns:
            self.cache.set_cache(cooldown.get('name'), cooldown)
        self.bot.log.info(f'Finished pre-caching {len(cooldowns)} cooldowns.')

    async def on_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cache.get_cache(cd_name)
        if entry is None:
            entry = await self.cds.find_one({'name': cd_name})
            self.cache.set_cache(cd_name, entry)
        if entry:
            end_stamp = entry.get('end_stamp', 0)
            now_stamp = arrow.utcnow().timestamp
            if now_stamp > end_stamp:
                cooldown = False
            else:
                cooldown = True
        else:
            cooldown = False
        return cooldown

    async def get_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cache.get_cache(cd_name)
        if entry is None:
            entry = await self.cds.find_one({'name': cd_name})
            self.cache.set_cache(cd_name, entry)
        if entry:
            end_stamp = entry.get('end_stamp', 0)
            now_stamp = arrow.utcnow().float_timestamp
            cooldown = end_stamp - now_stamp
            if cooldown < 2:
                if cooldown <= 0:
                    cooldown = 0.01
                else:
                    cooldown = round(cooldown, 2)
            else:
                cooldown = int(cooldown)
        else:
            cooldown = 0
        return cooldown

    async def set_cooldown(self, cmd, user, amount):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            if user.id in self.bot.cfg.dsc.owners:
                amount = 0
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        end_stamp = arrow.utcnow().timestamp + amount
        if entry:
            await self.cds.update_one({'name': cd_name}, {'$set': {'end_stamp': end_stamp}})
        else:
            cd_data = {'name': cd_name, 'end_stamp': end_stamp}
            await self.cds.insert_one(cd_data)
        self.cache.del_cache(cd_name)

    async def clean_cooldowns(self):
        now = arrow.utcnow().timestamp
        await self.cds.delete_many({'end_stamp': {'$lt': now}})
