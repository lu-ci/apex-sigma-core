import discord

from sigma.core.mechanics.config import load_config


class ApexSigma(discord.AutoShardedClient):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.log = self.init_logger()

    @staticmethod
    def init_logger():
        from sigma.core.mechanics.logger import create_logger
        log = create_logger('Sigma')
        return log

    def run(self):
        try:
            super().run(self.cfg.dsc.token)
        except discord.LoginFailure:
            self.log.error('Invalid Token!')
            exit()

    async def on_ready(self):
        self.log.info(f'Logged in as {self.user.name}')

    async def on_message(self, message):
        if message.author.id in self.cfg.dsc.owners:
            self.log.info(f'My owner {message.author.name} sent a message.')
