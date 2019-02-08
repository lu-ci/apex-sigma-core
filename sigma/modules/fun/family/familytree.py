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

import os
import json

import aiohttp

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, ok
from sigma.modules.fun.family.models.human import AdoptableHuman


async def familytree(cmd: SigmaCommand, pld: CommandPayload):
    target, is_self = (pld.msg.mentions[0], False) if pld.msg.mentions else (pld.msg.author, True)
    human = AdoptableHuman()
    await human.load(cmd.db, target.id)
    if human.exists:
        tree_data = human.draw_tree()
        async with aiohttp.ClientSession() as session:
            async with session.post('https://hastebin.com/documents', data=tree_data) as response:
                data = json.loads(await response.read())
        haste_url = f"https://hastebin.com/{data.get('key')}.yml"
        response = ok('Family tree file exported.')
        response.description = f'You can view it [here on hastebin]({haste_url}).'
    else:
        starter, ender = ('You may', 'you') if is_self else (f'{target.name} might', 'them')
        response = error(f'{starter} not have a family, but I\'ll always love {ender}.')
    await pld.msg.channel.send(embed=response)
