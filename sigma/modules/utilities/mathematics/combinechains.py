# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error


def combine_names(users: list):
    pieces = []
    total_length = sum([len(u.name) for u in users])
    usable_length = total_length // len(users)
    needed_length = usable_length // len(users)
    for user in users:
        piece = user.name[needed_length * len(pieces):needed_length * (len(pieces) + 1)]
        pieces.append(piece)
    return ''.join(pieces)


async def combinechains(cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.msg.mentions) >= 2:
        empty_chain = False
        chain_objects = []
        with ThreadPoolExecutor() as threads:
            for target in pld.msg.mentions:
                target_chain = await cmd.db[cmd.db.db_nam].MarkovChains.find_one({'user_id': target.id})
                if not target_chain:
                    empty_chain = target
                    break
                chain_string = ' '.join(target_chain.get('chain'))
                if not chain_string:
                    empty_chain = target
                    break
                cache_key = f'chain_{target.id}'
                markov_data = await cmd.db.cache.get_cache(cache_key)
                if not markov_data:
                    chain_task_one = functools.partial(markovify.Text, chain_string)
                    markov_data = await cmd.bot.loop.run_in_executor(threads, chain_task_one)
                    await cmd.db.cache.set_cache(cache_key, markov_data)
                chain_objects.append(markov_data)
            combination_id = '_'.join(sorted([str(u.id) for u in pld.msg.mentions]))
            combination_key = f"mixed_chain_{combination_id}"
            failed = False
            combination = await cmd.db.cache.get_cache(combination_key)
            if not combination:
                try:
                    combine_task = functools.partial(markovify.combine, chain_objects, [1] * len(chain_objects))
                    combination = await cmd.bot.loop.run_in_executor(threads, combine_task)
                    await cmd.db.cache.set_cache(combination_key, combination)
                except ValueError:
                    failed = True
            if not empty_chain:
                if not failed:
                    await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, 20)
                    sentence_function = functools.partial(combination.make_short_sentence, 500)
                    sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                    if not sentence:
                        not_enough_data = '😖 I could not think of anything... I need more chain items!'
                        response = discord.Embed(color=0xBE1931, title=not_enough_data)
                    else:
                        combined_name = combine_names(pld.msg.mentions)
                        response = discord.Embed(color=0xbdddf4)
                        response.set_author(name=combined_name, icon_url=user_avatar(secrets.choice(pld.msg.mentions)))
                        response.add_field(name='💭 Hmm... something like...', value=sentence)
                else:
                    response = error('Failed to combine the markov chains.')
            else:
                response = error(f'{empty_chain.name} does not have a chain.')
    else:
        response = error('Invalid number of targets.')
    await pld.msg.channel.send(embed=response)
