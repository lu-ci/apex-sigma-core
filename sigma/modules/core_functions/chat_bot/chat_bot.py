import functools
from concurrent.futures import ThreadPoolExecutor

import discord
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

cb = None


def clean_mentions(members, text):
    text = str(text)
    args = text.split(' ')
    out = []
    for arg in args:
        if arg.startswith('<@') and arg.endswith('>'):
            try:
                uid = arg[2:-1]
                user = discord.utils.find(lambda x: x.id == int(uid), members)
                if user:
                    addition = user.name
                else:
                    addition = 'Someone'
            except ValueError:
                addition = 'Someone'
        else:
            addition = arg
        out.append(addition)
    return ' '.join(out)


def init_chatterbot(ev):
    global cb
    if ev.db.chatterbot.statements.count():
        train = False
    else:
        train = True
    cb = ChatBot(
        "Sigma",
        database='chatterbot',
        database_uri=ev.db.db_address,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
    )
    if train:
        ev.log.info('Training Chatterbot...')
        cb.set_trainer(ChatterBotCorpusTrainer)
        cb.train('chatterbot.corpus.english')
        ev.log.info('Chatterbot Training Complete')


async def chat_bot(ev, message):
    if not cb:
        init_chatterbot(ev)
    args = message.content.split(' ')
    if len(args) > 1:
        if args[1].lower() not in ev.bot.modules.alts:
            if args[1].lower() not in ev.bot.modules.commands:
                if message.guild:
                    active = ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
                    if active:
                        mention = f'<@{ev.bot.user.id}>'
                        mention_alt = f'<@!{ev.bot.user.id}>'
                        if message.content.startswith(mention) or message.content.startswith(mention_alt):
                            interaction = ' '.join(args[1:])
                            if interaction:
                                task = functools.partial(cb.get_response, interaction)
                                with ThreadPoolExecutor() as threads:
                                    cb_resp = await ev.bot.loop.run_in_executor(threads, task)
                                cb_resp = clean_mentions(ev.bot.get_all_members(), cb_resp)
                                response = f'{message.author.mention} {cb_resp}'
                                await message.channel.send(response)
