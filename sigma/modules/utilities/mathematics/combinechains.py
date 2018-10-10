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
import secrets
from concurrent.futures import ThreadPoolExecutor

import discord
import markovify

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.utilities.mathematics.impersonate import chain_object_cache

combination_cache = Cacher()


def combine_names(users: list):
    pieces = []
    total_length = sum([len(u.name) for u in users])
    usable_length = total_length // len(users)
    needed_length = usable_length // len(users)
    for user in users:
        piece = user.name[needed_length * len(pieces):needed_length * (len(pieces) + 1)]
        pieces.append(piece)
    return ''.join(pieces)


async def combinechains(cmd: SigmaCommand, message: discord.Message, args: list):
    if len(message.mentions) >= 2:
        empty_chain = False
        chain_objects = []
        with ThreadPoolExecutor() as threads:
            for target in message.mentions:
                target_chain = await cmd.db[cmd.db.db_nam].MarkovChains.find_one({'user_id': target.id})
                if not target_chain:
                    empty_chain = target
                    break
                chain_string = ' '.join(target_chain.get('chain'))
                if not chain_string:
                    empty_chain = target
                    break
                markov_data = chain_object_cache.get_cache(target.id)
                if not markov_data:
                    chain_task_one = functools.partial(markovify.Text, chain_string)
                    markov_data = await cmd.bot.loop.run_in_executor(threads, chain_task_one)
                    chain_object_cache.set_cache(target.id, markov_data)
                chain_objects.append(markov_data)
            combination_key = '_'.join(sorted([str(u.id) for u in message.mentions]))
            combination = combination_cache.get_cache(combination_key)
            if not combination:
                combine_task = functools.partial(markovify.combine, chain_objects, [1] * len(chain_objects))
                combination = await cmd.bot.loop.run_in_executor(threads, combine_task)
                combination_cache.set_cache(combination_key, combination)
            if not empty_chain:
                await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, 20)
                sentence_function = functools.partial(combination.make_short_sentence, 500)
                sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                if not sentence:
                    not_enough_data = '😖 I could not think of anything... I need more chain items!'
                    response = discord.Embed(color=0xBE1931, title=not_enough_data)
                else:
                    combined_name = combine_names(message.mentions)
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=combined_name, icon_url=user_avatar(secrets.choice(message.mentions)))
                    response.add_field(name='💭 Hmm... something like...', value=sentence)
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ {empty_chain.name} does not have a chain.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Invalid number of targets.')
    await message.channel.send(embed=response)
