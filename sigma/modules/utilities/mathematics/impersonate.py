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
import markovify

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar

chain_object_cache = Cacher(True, 3600)


async def impersonate(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.guild.members)
    else:
        target = message.author
    if target:
        chain_data = await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target.id})
        if chain_data:
            if chain_data['Chain']:
                total_string = ' '.join(chain_data['Chain'])
                chain_function = functools.partial(markovify.Text, total_string)
                with ThreadPoolExecutor() as threads:
                    chain = chain_object_cache.get_cache(target.id)
                    if not chain:
                        chain = await cmd.bot.loop.run_in_executor(threads, chain_function)
                        chain_object_cache.set_cache(target.id, chain)
                    sentence_function = functools.partial(chain.make_short_sentence, 500)
                    sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                if not sentence:
                    not_enough_data = '😖 I could not think of anything... I need more chain items!'
                    response = discord.Embed(color=0xBE1931, title=not_enough_data)
                else:
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=target.name, icon_url=user_avatar(target))
                    response.add_field(name='💭 Hmm... something like...', value=sentence)
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ {target.name}\'s chain has no data.')
        else:
            response = discord.Embed(color=0x696969)
            prefix = await cmd.db.get_prefix(message)
            title = f'🔍 Chain Data Not Found For {target.name}'
            value = f'You can make one with `{prefix}collectchain @{target.name} #channel`!'
            response.add_field(name=title, value=value)
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
