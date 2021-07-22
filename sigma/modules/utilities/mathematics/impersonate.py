"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import functools
import os
from concurrent.futures import ThreadPoolExecutor

import discord
import markovify

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.mathematics.collector_clockwork import deserialize, load


def get_target_and_args(pld):
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
        for arg in pld.args:
            if str(target.id) in arg:
                pld.args.pop(pld.args.index(arg))
                break
    else:
        target = pld.msg.author

    limit = 500
    beginning = None
    if pld.args:
        if pld.args[0].isdigit():
            limit = int(pld.args.pop(0))
        else:
            beginning = ' '.join(pld.args[:2])
    return target, limit, beginning


async def impersonate(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target, limit, beginning = get_target_and_args(pld)
    if target:
        if os.path.exists(f'chains/{target.id}.json.gz'):
            chain_data = load(target.id)
            if chain_data:
                chain_function = functools.partial(markovify.Text.from_dict, deserialize(chain_data))
                with ThreadPoolExecutor() as threads:
                    try:
                        chain = await cmd.bot.loop.run_in_executor(threads, chain_function)
                        if beginning:
                            sentence_func = chain.make_sentence_with_start
                            sentence_args = [beginning, False]
                        else:
                            sentence_func = chain.make_short_sentence
                            sentence_args = [limit]
                        sentence_function = functools.partial(sentence_func, *sentence_args, tries=20)
                        sentence = await cmd.bot.loop.run_in_executor(threads, sentence_function)
                    except (KeyError, ValueError, AttributeError):
                        sentence = None
                    except markovify.text.ParamError:
                        if not beginning:
                            sentence = None
                        else:
                            ender = 'word' if len(beginning.split()) == 1 else 'phrase'
                            response = GenericResponse(f'Your chain does not contain that {ender}').error()
                            await pld.msg.channel.send(embed=response)
                            return
                if not sentence:
                    not_enough_data = '😖 I could not think of anything... I need more chain items!'
                    response = discord.Embed(color=0xBE1931, title=not_enough_data)
                else:
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=target.name, icon_url=user_avatar(target))
                    response.add_field(name='💭 Hmm... something like...', value=sentence)
            else:
                response = GenericResponse(f'{target.name}\'s chain has no data.').error()
        else:
            response = discord.Embed(color=0x696969)
            prefix = cmd.db.get_prefix(pld.settings)
            title = f'🔍 Chain Data Not Found For {target.name}'
            value = f'You can make one with `{prefix}collectchain @{target.name} #channel`!'
            response.add_field(name=title, value=value)
    else:
        response = GenericResponse('No user targeted.').error()
    await pld.msg.channel.send(embed=response)
