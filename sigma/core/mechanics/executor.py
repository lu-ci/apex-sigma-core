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

import asyncio

import discord

from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.payload import MessagePayload, CommandPayload, SigmaPayload
from sigma.core.mechanics.statistics import StatisticsStorage


class ExecutionClockwork(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Threader')
        self.ev_queue = asyncio.Queue()
        self.cmd_queue = asyncio.Queue()
        self.bot.loop.create_task(self.queue_ev_loop())
        self.bot.loop.create_task(self.queue_cmd_loop())
        self.processed = 0
        self.stats = {}

    async def get_cmd_and_args(self, message: discord.Message, args: list):
        args = list(filter(lambda a: a != '', args))
        pfx = await self.bot.db.get_prefix(message)
        cmd = args.pop(0)[len(pfx):].lower()
        return cmd, args

    async def command_runner(self, pld: MessagePayload):
        if self.bot.ready:
            prefix = await self.bot.db.get_prefix(pld.msg)
            if pld.msg.content.startswith(prefix):
                args = pld.msg.content.split(' ')
                cmd, args = await self.get_cmd_and_args(pld.msg, args)
                cmd = self.bot.modules.alts.get(cmd) if cmd in self.bot.modules.alts else cmd
                command = self.bot.modules.commands.get(cmd)
                if command:
                    if self.bot.cfg.pref.text_only and command.category == 'music':
                        return
                    elif self.bot.cfg.pref.music_only and command.category != 'music':
                        return
                    else:
                        cmd_pld = CommandPayload(self.bot, pld.msg, args)
                        task = command, cmd_pld
                        await self.cmd_queue.put(task)

    def get_stats_storage(self, event):
        stats_handler = self.stats.get(event)
        if not stats_handler:
            stats_handler = StatisticsStorage(self.bot.db, event)
            self.stats.update({event: stats_handler})
        return stats_handler

    async def event_runner(self, event_name: str, pld: SigmaPayload = None):
        if self.bot.ready:
            if event_name in self.bot.modules.events:
                if pld:
                    await pld.init()
                self.get_stats_storage(event_name).add_stat()
                for event in self.bot.modules.events[event_name]:
                    task = event, pld
                    await self.ev_queue.put(task)

    async def queue_ev_loop(self):
        while True:
            if self.bot.ready:
                item, pld = await self.ev_queue.get()
                self.bot.loop.create_task(item.execute(pld))
                self.processed += 1
            else:
                await asyncio.sleep(1)

    async def queue_cmd_loop(self):
        while True:
            if self.bot.ready:
                item, pld = await self.cmd_queue.get()
                self.bot.loop.create_task(item.execute(pld))
                self.processed += 1
            else:
                await asyncio.sleep(1)
