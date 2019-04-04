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

from io import BytesIO

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.fun.family.models.human import AdoptableHuman


async def familytree(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    tree_file = None
    response = None
    text_response = None
    target, is_self = (pld.msg.mentions[0], False) if pld.msg.mentions else (pld.msg.author, True)
    human = AdoptableHuman(cmd.db, target.id)
    await human.load()
    if human.exists:
        top_parent = human.top_parent()
        new_top_parent = AdoptableHuman(cmd.db, top_parent.id, False, True)
        await new_top_parent.load()
        tree_data = new_top_parent.draw_tree(human.id)
        io = BytesIO()
        io.write(tree_data.encode('utf-8'))
        io.seek(0)
        text_response = '✅ Family tree file exported.'
        tree_file = discord.File(io, f'family_tree_{pld.msg.id}.yml')
    else:
        starter, ender = ('You may', 'you') if is_self else (f'{target.name} might', 'them')
        response = error(f'{starter} not have a family, but I\'ll always love {ender}.')
    await pld.msg.channel.send(text_response, file=tree_file, embed=response)
