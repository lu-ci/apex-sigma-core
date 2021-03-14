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

import asyncio

import arrow

from sigma.modules.minigames.professions.market.market_models import MarketEntry
from sigma.modules.minigames.professions.nodes.item_core import get_item_core

ME_LOOP_RUNNING = False
MARKET_LIFETIME = 60 * 60 * 24 * 7


async def market_expiration(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global ME_LOOP_RUNNING
    if not ME_LOOP_RUNNING:
        ME_LOOP_RUNNING = True
        ev.bot.loop.create_task(cycler(ev))


async def check_expiry(db):
    """
    :type db: sigma.core.mechanics.database.Database
    """
    now = arrow.utcnow().timestamp()
    ic = await get_item_core(db)
    async for ed in db[db.db_nam].MarketEntries.find({'stamp': {'$lt': now - MARKET_LIFETIME}}):
        entry = MarketEntry(ed)
        item = ic.get_item_by_file_id(entry.item)
        if item:
            data_for_inv = item.generate_inventory_item()
            await db.add_to_inventory(entry.uid, data_for_inv)
        await entry.delete(db)


async def cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        await check_expiry(ev.db)
        await asyncio.sleep(60)
