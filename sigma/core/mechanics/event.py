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

import discord

from sigma.core.mechanics.exceptions import DummyException
from sigma.core.mechanics.logger import create_logger


class SigmaEvent(object):
    """
    The core event class for handling and executing event functions.
    """

    __slots__ = (
        "bot", "db", "event", "module_info", "event_info",
        "path", "event_type", "name", "description",
        "category", "subcategory", "log"
    )

    def __init__(self, bot, event, module_info, event_info):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :type event: function
        :type module_info: dict
        :type event_info: dict
        """
        self.bot = bot
        self.db = self.bot.db
        self.event = event
        self.module_info = module_info
        self.event_info = event_info
        self.path = self.event_info.get('path')
        self.event_type = self.event_info.get('type')
        self.name = self.event_info.get('name')
        self.category = self.module_info.get('category')
        self.description = self.event_info.get('description')
        self.subcategory = self.module_info.get('subcategory')
        self.log = create_logger(self.name.upper(), shards=self.bot.cfg.dsc.shards)

    def get_exception(self):
        """
        Returns a dummy exception if in developer mode.
        A dummy exception should never be raised.
        :rtype: Exception
        """
        if self.bot.cfg.pref.dev_mode:
            ev_exception = DummyException
        else:
            ev_exception = Exception
        return ev_exception

    def log_error(self, exception):
        """
        Adds a line in the logger in case something breaks.
        :type exception: Exception
        """
        log_text = f'ERROR: {exception} | TRACE: {exception.with_traceback}'
        self.log.error(log_text)

    def resource(self, res_path):
        """
        Gets the module resource path.
        :type res_path: str
        :rtype: str
        """
        module_path = self.path
        res_path = f'{module_path}/res/{res_path}'
        res_path = res_path.replace('\\', '/')
        return res_path

    async def execute(self, pld=None):
        """
        The main event executor function.
        :type pld: sigma.core.mechanics.payload.SigmaPayload
        """
        if self.bot.ready or self.event_type in ['dbinit', 'boot']:
            try:
                if pld:
                    await getattr(self.event, self.name)(self, pld)
                else:
                    await getattr(self.event, self.name)(self)
            except discord.Forbidden:
                pass
            except self.get_exception() as e:
                self.log_error(e)
