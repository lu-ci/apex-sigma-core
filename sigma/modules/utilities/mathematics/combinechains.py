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

import json
import os
import secrets

import aiohttp
import discord
import markovify

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.mathematics.collector_clockwork import deserialize, load
from sigma.modules.utilities.mathematics.impersonate import ensure_length, parse_args


def shuffle(items):
    """
    :type items: list[discord.Member]
    :rtype: list[discord.Member]
    """
    new = []
    copy = [i for i in items]
    while len(copy) > 0:
        new.append(copy.pop(secrets.randbelow(len(copy))))
    return new


def combine_names(users):
    """
    :type users: list[discord.Member]
    :rtype: str
    """
    pieces = []
    users = shuffle(users)
    total_length = sum([len(u.name) for u in users])
    usable_length = total_length // len(users)
    needed_length = usable_length // len(users)
    for user in users:
        piece = user.name[needed_length * len(pieces):needed_length * (len(pieces) + 1)]
        pieces.append(piece)
    return ''.join(pieces)


async def combinechains_server(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    cfg = cmd.bot.modules.commands.get('impersonate').cfg
    server = cfg.get("server")
    targets, _, beginning = parse_args(pld, True)
    if targets:
        target_ids = [str(target.id) for target in targets]
        normal = f'{server}/combined/{",".join(target_ids)}'
        seeded = f'{normal}?seed={beginning}'
        uri = seeded if beginning else normal
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.read())
                    sentence = data.get('sentence', "").strip()
                    if sentence:
                        time = round(data.get("time"), 5)
                        sntcs = data.get("sentences")
                        cells = data.get("cells")
                        footer = f'Response generated in {time}s from {sntcs} sentences made out of {cells} cells.'
                        combined_name = combine_names(targets)
                        response = discord.Embed(color=0xbdddf4)
                        response.set_author(name=combined_name, icon_url=user_avatar(secrets.choice(targets)))
                        response.add_field(name='💭 Hmm... something like...', value=ensure_length(sentence))
                        response.set_footer(text=footer)
                    else:
                        ender = 'word' if len(beginning.split()) == 1 else 'phrase'
                        error_title = f'😖 I could not think of anything with that {ender}.'
                        response = discord.Embed(color=0xBE1931, title=error_title)
                elif resp.status == 404:
                    response = discord.Embed(color=0x696969)
                    prefix = cmd.db.get_prefix(pld.settings)
                    title = f'🔍 One or more tagged users do not have chains.'
                    value = f'You can make one with `{prefix}collectchain @target #channel`!'
                    response.add_field(name=title, value=value)
                else:
                    response = GenericResponse("An unknown error ocurred, please try again...").error()
                    response.description = f'Message: {await resp.text()}'
    else:
        response = GenericResponse('No user targeted.').error()
    await pld.msg.channel.send(embed=response)


async def combinechains_local(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.msg.mentions) >= 2:
        empty_chain = None
        chains = []
        chain_dicts = []
        targets, limit, beginning = parse_args(pld, True)
        for target in targets:
            target_chain = None
            if os.path.exists(f'chains/{target.id}.json.gz'):
                target_chain = await cmd.bot.threader.execute(load, (target.id,))
            if not target_chain:
                empty_chain = target
                break
            chain_dicts.append(await cmd.bot.threader.execute(deserialize, (target_chain, )))
        if not empty_chain:
            failed = False
            for chain_dict in chain_dicts:
                try:
                    chain = await cmd.bot.threader.execute(markovify.Text.from_dict, (chain_dict,))
                    chains.append(chain)
                except (ValueError, KeyError, AttributeError):
                    failed = True
                    break
            if not failed:
                await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, 20)
                try:
                    combination = await cmd.bot.threader.execute(markovify.combine, (chains,))
                    if beginning:
                        sentence_func = combination.make_sentence_with_start
                        sentence_args = (beginning, False,)
                    else:
                        sentence_func = combination.make_short_sentence
                        sentence_args = (limit,)
                    sentence = await cmd.bot.threader.execute(sentence_func, sentence_args)
                except (ValueError, KeyError, AttributeError):
                    sentence = None
                except markovify.text.ParamError:
                    if not beginning:
                        sentence = None
                    else:
                        ender = 'word' if len(beginning.split()) == 1 else 'phrase'
                        error_title = f'😖 I could not think of anything with that {ender}.'
                        response = discord.Embed(color=0xBE1931, title=error_title)
                        await pld.msg.channel.send(embed=response)
                        return
                if not sentence:
                    not_enough_data = '😖 I could not think of anything... I need more chain items!'
                    response = discord.Embed(color=0xBE1931, title=not_enough_data)
                else:
                    combined_name = combine_names(targets)
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=combined_name, icon_url=user_avatar(secrets.choice(targets)))
                    response.add_field(name='💭 Hmm... something like...', value=ensure_length(sentence))
            else:
                response = GenericResponse('Failed to combine the markov chains.').error()
        else:
            response = GenericResponse(f'{empty_chain.name} does not have a chain.').error()
    else:
        response = GenericResponse('Invalid number of targets.').error()
    await pld.msg.channel.send(embed=response)


async def combinechains(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    cfg = cmd.bot.modules.commands.get('impersonate').cfg
    server = cfg.get("server")
    if server:
        await combinechains_server(cmd, pld)
    else:
        await combinechains_local(cmd, pld)
