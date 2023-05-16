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


class StatisticsStorage(object):
    """
    Statistics handling class to reduce database load.
    Updates the statistics every 60 seconds instead of instantly.
    """

    __slots__ = ("db", "loop", "name", "count")

    def __init__(self, db, name):
        """
        :type db: sigma.core.mechanics.database.Database
        :type name: str
        """
        self.db = db
        self.loop = asyncio.get_event_loop()
        self.name = name
        self.count = 0
        self.loop.create_task(self.insert_stats())

    def add_stat(self):
        """
        Increments the current statistic by one.
        """
        self.count += 1

    async def insert_stats(self):
        """
        An infinite loop that dumps the statistics in the database every 60 seconds.
        """
        while True:
            def_stat_data = {'event': self.name, 'count': 0}
            collection = 'EventStats'
            database = self.db.db_nam
            check = await self.db[database][collection].find_one({"event": self.name})
            if not check:
                await self.db[database][collection].insert_one(def_stat_data)
                ev_count = 0
            else:
                ev_count = check.get('count', 0)
            ev_count += self.count
            update_target = {"event": self.name}
            update_data = {"$set": {'count': ev_count}}
            await self.db[database][collection].update_one(update_target, update_data)
            self.count = 0
            await asyncio.sleep(60)


class CommandStatistic(object):
    __slots__ = ('db', 'cmd', 'pld', 'coll', 'exec_time', 'exec_timestamp')

    def __init__(self, db, cmd, pld):
        """
        :type db: sigma.core.mechanics.database.Database
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        :type pld: sigma.core.mechanics.payload.CommandPayload
        """
        self.db = db
        self.cmd = cmd
        self.pld = pld
        self.coll = self.db[self.db.db_nam].DetailedCommandStats
        self.exec_time = None
        self.exec_timestamp = None

    def to_dict(self):
        """
        :rtype: dict
        """
        return {
            'command': {
                'name': self.cmd.name,
                'category': self.cmd.category,
                'nsfw': self.cmd.nsfw,
                'execution': {
                    'time': self.exec_time,
                    'timestamp': self.exec_timestamp,
                    'formatted': arrow.get(self.exec_timestamp).format()
                }
            },
            'message': {
                'id': self.pld.msg.id,
                'content': self.pld.msg.content,
                'arguments': self.pld.args,
                'created_at': arrow.get(self.pld.msg.created_at).format()
            },
            'user': {
                'id': self.pld.msg.author.id,
                'name': self.pld.msg.author.name,
                'discriminator': self.pld.msg.author.discriminator,
                'display_name': self.pld.msg.author.display_name
            },
            'channel': {
                'id': self.pld.msg.channel.id if self.pld.msg.guild else None,
                'name': self.pld.msg.channel.name if self.pld.msg.guild else None
            },
            'guild': {
                'id': self.pld.msg.guild.id if self.pld.msg.guild else None,
                'name': self.pld.msg.guild.name if self.pld.msg.guild else None
            }
        }

    async def save(self):
        await self.coll.insert_one(self.to_dict())
