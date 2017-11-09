def log_dm(ev, message):
    author_text = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
    ev.log.info(f'DM From {author_text}: {message.content}')


async def dm_detection(ev, message):
    if not message.guild:
        if not message.author.bot:
            pfx = ev.bot.get_prefix(message)
            if not message.content.startswith(pfx):
                log_dm(ev, message)
                await ev.bot.modules.commands['help'].execute(message, [])
