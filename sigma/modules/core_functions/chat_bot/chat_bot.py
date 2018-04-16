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
    try:
        if not cb:
            init_chatterbot(ev)
        args = message.content.split(' ')
        if len(args) > 1:
            if message.guild:
                active = await ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
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
    except IndexError:
        pass
