# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import asyncio

from sigma.core.mechanics.logger import create_logger


class QueueControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Threader')
        self.queue = asyncio.Queue()
        self.bot.loop.create_task(self.queue_loop())
        self.processed = 0

    async def queue_loop(self):
        while True:
            if self.bot.ready:
                item, *args = await self.queue.get()
                self.bot.loop.create_task(item.execute(*args))
                self.processed += 1
            else:
                await asyncio.sleep(1)
