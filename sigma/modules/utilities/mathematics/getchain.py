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


async def get_chain(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    embed = None
    text = None
    file = None
    fname = f'{pld.msg.author.id}.json.gz'
    path = f'chains/{fname}'
    if os.path.exists(path):
        text = f'Here\'s your chain file, {pld.msg.author.name}.'
        file = discord.File(path, fname)
    else:
        embed = GenericResponse('You don\'t seem to have a chain file.').not_found()
    await pld.msg.channel.send(text, embed=embed, file=file)


