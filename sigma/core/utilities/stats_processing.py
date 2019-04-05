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

from sigma.core.mechanics.statistics import StatisticsStorage

stats_handler = None


async def add_cmd_stat(cmd):
    """
    Increments the usage count for this command by one.
    :param cmd: The command to increment stats for.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    """
    lookup_target = {'command': cmd.name}
    stat_file = await cmd.db[cmd.db.db_nam].CommandStats.find_one(lookup_target)
    if stat_file:
        count = (stat_file.get('count') or 0) + 1
        await cmd.db[cmd.db.db_nam].CommandStats.update_one(lookup_target, {'$set': {'count': count}})
    else:
        count = 1
        await cmd.db[cmd.db.db_nam].CommandStats.insert_one({'command': cmd.name, 'count': count})


async def add_special_stats(db, stat_name):
    """
    Increments the usage count for this statistic by one.
    :param db: The core database instance.
    :type db: sigma.core.mechanics.database.Database
    :param stat_name: The name of the statistic to track.
    :type stat_name: str
    """
    global stats_handler
    if not stats_handler:
        stats_handler = StatisticsStorage(db, stat_name)
    stats_handler.add_stat()
