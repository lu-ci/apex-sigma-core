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

from sigma.core.mechanics.event import SigmaEvent

cb_cache = None
inter_cache = {}


def get_cb(db):
    global cb_cache
    if not cb_cache:
        cb_cache = ChatBot(
            "Sigma",
            database='chatterbot',
            database_uri=db.db_address,
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            output_format='text'
        )
    return cb_cache


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


async def chat_bot(ev: SigmaEvent, message: discord.Message):
    try:
        args = message.content.split(' ')
        if len(args) > 1 and len(message.content) < 512:
            if message.guild:
                active = await ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
                if active:
                    mention = f'<@{ev.bot.user.id}>'
                    mention_alt = f'<@!{ev.bot.user.id}>'
                    if message.content.startswith(mention) or message.content.startswith(mention_alt):
                        interaction = ' '.join(args[1:])
                        if interaction:
                            cb = get_cb(ev.db)
                            conversation = message.channel.id
                            async with message.channel.typing():
                                with ThreadPoolExecutor() as threads:
                                    interaction_task = functools.partial(cb.input.process_input_statement, interaction)
                                    interaction = await ev.bot.loop.run_in_executor(threads, interaction_task)
                                    response_task = functools.partial(cb.generate_response, interaction, conversation)
                                    _, response = await ev.bot.loop.run_in_executor(threads, response_task)
                                    output_task = functools.partial(cb.output.process_response, response)
                                    await ev.bot.loop.run_in_executor(threads, output_task)
                                cb_resp = clean_mentions(ev.bot.get_all_members(), response)
                                response = f'{message.author.mention} {cb_resp}'
                                await message.channel.send(response)
                                ev.log.info(f'{message.author.name}: {interaction} | {ev.bot.user.name}: {cb_resp}')
    except IndexError:
        pass
