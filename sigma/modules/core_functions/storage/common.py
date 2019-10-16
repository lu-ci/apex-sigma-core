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

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig

OBJECT_EXISTENCE_CACHE = MemoryCacher(CacheConfig({}))


async def object_exists(db, variant, oid):
    """
    Checks if an object with the given ID exists in the object storage.
    :param db: The database client.
    :type db: sigma.core.mechanics.database.Database
    :param variant: The type of object to grab.
    :type variant: str
    :param oid: The ID of the object.
    :type oid: int
    :return: bool
    """
    timeout = 60
    key = f'{variant}_{oid}'
    stamp_key = f'{variant}_{oid}_stamp'
    exists = await OBJECT_EXISTENCE_CACHE.get_cache(key)
    now = arrow.utcnow().timestamp
    timestamp = await OBJECT_EXISTENCE_CACHE.get_cache(stamp_key) or 0
    if exists is None or now > timestamp + timeout:
        coll = db[db.db_nam][f'{variant.title()}Objects']
        exists = bool(await coll.count_documents({'id': oid}))
        await OBJECT_EXISTENCE_CACHE.set_cache(key, exists)
    return exists
