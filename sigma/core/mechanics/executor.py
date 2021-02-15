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

from sigma.core.mechanics.payload import CommandPayload
from sigma.core.mechanics.statistics import StatisticsStorage


class ExecutionClockwork(object):
    """
    This acts as a queueing mechanism for tasks to be executed.
    """

    __slots__ = ("bot", "ev_queue", "cmd_queue", "processed", "stats")

    def __init__(self, bot):
        """
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.ev_queue = asyncio.Queue()
        self.cmd_queue = asyncio.Queue()
        self.bot.loop.create_task(self.queue_ev_loop())
        self.bot.loop.create_task(self.queue_cmd_loop())
        self.processed = 0
        self.stats = {}

    @staticmethod
    async def get_cmd_and_args(pfx, args):
        """
        Gets the command name and arguments from a message.
        :type pfx: str
        :type args: list[str]
        :rtype: (str, list[str])
        """
        args = list(filter(lambda a: a != '', args))
        cmd = args.pop(0)[len(pfx):].lower()
        return cmd, args

    async def command_runner(self, pld):
        """
        Function in charge of getting a command ready for the queue.
        :param pld: The message payload data that triggers the command.
        :type pld: sigma.core.mechanics.payload.MessagePayload
        """
        if self.bot.ready:
            await pld.init()
            prefix = self.bot.db.get_prefix(pld.settings)
            if pld.msg.content.startswith(prefix):
                args = pld.msg.content.split(' ')
                cmd, args = await self.get_cmd_and_args(prefix, args)
                cmd = self.bot.modules.alts.get(cmd) if cmd in self.bot.modules.alts else cmd
                command = self.bot.modules.commands.get(cmd)
                if command:
                    cmd_pld = CommandPayload(self.bot, pld.msg, args)
                    cmd_pld.settings = pld.settings
                    task = command, cmd_pld
                    await self.cmd_queue.put(task)

    def get_stats_storage(self, event):
        """
        Gets the statistics handler for the given event.
        :type event: str
        :rtype: sigma.core.mechanics.statistics.StatisticsStorage
        """
        stats_handler = self.stats.get(event)
        if not stats_handler:
            stats_handler = StatisticsStorage(self.bot.db, event)
            self.stats.update({event: stats_handler})
        return stats_handler

    async def event_runner(self, event_name, pld=None):
        """
        Function in charge of getting events ready for the queue.
        :type event_name: str
        :param pld: The payload data of the event.
        :type pld: sigma.core.mechanics.payload.SigmaPayload
        """
        if self.bot.ready:
            if event_name in self.bot.modules.events:
                if pld:
                    await pld.init()
                self.get_stats_storage(event_name).add_stat()
                for event in self.bot.modules.events[event_name]:
                    task = event, pld
                    await self.ev_queue.put(task)

    async def queue_ev_loop(self):
        """
        Infinite loop that executes queued events.
        """
        while True:
            if self.bot.ready:
                item, pld = await self.ev_queue.get()
                self.bot.loop.create_task(item.execute(pld))
                self.processed += 1
            else:
                await asyncio.sleep(1)

    async def queue_cmd_loop(self):
        """
        Infinite loop that executes queued commands.
        """
        while True:
            if self.bot.ready:
                item, pld = await self.cmd_queue.get()
                self.bot.loop.create_task(item.execute(pld))
                self.processed += 1
            else:
                await asyncio.sleep(1)
