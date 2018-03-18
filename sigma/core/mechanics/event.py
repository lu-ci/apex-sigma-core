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

import discord

from sigma.core.mechanics.exceptions import DummyException
from sigma.core.mechanics.logger import create_logger


class SigmaEvent(object):
    def __init__(self, bot, event, plugin_info, event_info):
        self.bot = bot
        self.db = self.bot.db
        self.event = event
        self.plugin_info = plugin_info
        self.event_info = event_info
        self.event_type = self.event_info['type']
        self.name = self.event_info['name']
        self.category = self.plugin_info['category']
        self.log = create_logger(self.name.upper())

    def get_exception(self):
        if self.bot.cfg.pref.dev_mode:
            ev_exception = DummyException
        else:
            ev_exception = Exception
        return ev_exception

    def log_error(self, exception: Exception):
        log_text = f'ERROR: {exception} | TRACE: {exception.with_traceback}'
        self.log.error(log_text)

    async def execute(self, *args):
        if self.bot.ready:
            try:
                await getattr(self.event, self.name)(self, *args)
            except discord.Forbidden:
                pass
            except self.get_exception() as e:
                self.log_error(e)
