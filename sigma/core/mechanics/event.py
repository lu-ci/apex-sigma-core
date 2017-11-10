import os
import discord

from sigma.core.mechanics.module_component import SigmaModuleComponent
from sigma.core.mechanics.logger import create_logger

class SigmaEvent(SigmaModuleComponent):
    def __init__(self, module, config):
        super().__init__(module, config)

        self.log = create_logger(self.name.upper())
        self.module = module
        self.type = self.config['type']

    @property
    def event(self):
        return self.load_path(os.path.join(self.path, self.name))

    def get_exception(self):
        if self.bot.cfg.pref.dev_mode:
            cmd_exception = SyntaxError
        else:
            cmd_exception = Exception
        return cmd_exception

    def log_error(self, exception):
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
