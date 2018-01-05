import arrow
import discord

from sigma.core.mechanics.exceptions import DummyException
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.statistics import ElasticHandler


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
        if self.bot.cfg.pref.raw.get('elastic'):
            self.stats = ElasticHandler(self.bot.cfg.pref.raw.get('elastic'), 'sigma-event')
        else:
            self.stats = None

    def get_exception(self):
        if self.bot.cfg.pref.dev_mode:
            ev_exception = DummyException
        else:
            ev_exception = Exception
        return ev_exception

    def log_error(self, exception):
        log_text = f'ERROR: {exception} | TRACE: {exception.with_traceback}'
        self.log.error(log_text)

    async def add_elastic_stats(self):
        stat_data = {
            'event': self.name,
            'type': self.event_type,
            'category': self.category,
            'time': {
                'executed': {
                    'date': arrow.utcnow().format('YYYY-MM-DD'),
                    'stamp': arrow.utcnow().float_timestamp
                }
            }
        }
        await self.stats.push(stat_data)

    async def execute(self, *args):
        if self.bot.ready:
            try:
                await getattr(self.event, self.name)(self, *args)
                if self.stats:
                    await self.add_elastic_stats()
            except discord.Forbidden:
                pass
            except self.get_exception() as e:
                self.log_error(e)
