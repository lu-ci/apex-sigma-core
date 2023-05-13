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
import os

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.mathematics.collector_clockwork import deserialize, load


async def markovchain(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    collection = load(target.id) if os.path.exists(f'chains/{target.id}.json.gz') else None
    if collection:
        chain = deserialize(collection).get('parsed_sentences', [])
        starter = 'Your' if target.id == pld.msg.author.id else f'{target.name}\'s'
        response = discord.Embed(color=0xF9F9F9, title=f'⛓ {starter} chain corpus size is {len(chain)}.')
    else:
        starter = 'You don\'t have' if target.id == pld.msg.author.id else f'{target.name} doesn\'t have'
        response = GenericResponse(f'{starter} a collected chain.').not_found()
    await pld.msg.channel.send(embed=response)
