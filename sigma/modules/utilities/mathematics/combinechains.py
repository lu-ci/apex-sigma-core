# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

from sigma.core.utilities.data_processing import user_avatar


def combine_names(user_one, user_two):
    cutoff_one = len(user_one.name) // 2
    cutoff_two = len(user_two.name) // 2
    piece_one = user_one.name[:cutoff_one]
    piece_two = user_two.name[cutoff_two:]
    output = piece_one + piece_two
    return output


async def combinechains(cmd, message, args):
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
        if len(message.mentions) == 2:
            target_one = message.mentions[0]
            target_two = message.mentions[1]
            chain_one = await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target_one.id})
            chain_two = await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target_two.id})
            if chain_one and chain_two:
                await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, 20)
                init_embed = discord.Embed(color=0xbdddf4, title='💭 Hmm... Let me think...')
                init_message = await message.channel.send(embed=init_embed)
                string_one = ' '.join(chain_one.get('Chain'))
                string_two = ' '.join(chain_two.get('Chain'))
                with ThreadPoolExecutor() as threads:
                    chain_task_one = functools.partial(markovify.Text, string_one)
                    chain_task_two = functools.partial(markovify.Text, string_two)
                    markov_one = await cmd.bot.loop.run_in_executor(threads, chain_task_one)
                    markov_two = await cmd.bot.loop.run_in_executor(threads, chain_task_two)
                    combine_task = functools.partial(markovify.combine, [markov_one, markov_two], [1, 1])
                    combination = await cmd.bot.loop.run_in_executor(threads, combine_task)
                    sentence_function = functools.partial(combination.make_short_sentence, 500)
                    sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                if not sentence:
                    response = discord.Embed(color=0xBE1931, title='😖 I could not think of anything...')
                else:
                    icon_choice = secrets.choice([target_one, target_two])
                    combined_name = combine_names(target_one, target_two)
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=combined_name, icon_url=user_avatar(icon_choice))
                    response.add_field(name='💭 Hmm... something like...', value=sentence)
                await init_message.edit(embed=response)
            else:
                no_chain = discord.Embed(color=0xBE1931, title='❗ One of the users does not have a chain.')
                await message.channel.send(embed=no_chain)
        else:
            no_target = discord.Embed(color=0xBE1931, title='❗ Invalid number of targets.')
            await message.channel.send(embed=no_target)
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
        on_cooldown = discord.Embed(color=0xccffff, title=f'❄ On cooldown for another {timeout} seconds.')
        await message.channel.send(embed=on_cooldown)
