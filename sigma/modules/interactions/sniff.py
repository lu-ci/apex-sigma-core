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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.interactions.mech.interaction_mechanics import get_target, grab_interaction, make_footer

endings = ['themself', 'something off the table', 'panties', 'glue', ]


async def sniff(cmd: SigmaCommand, pld: CommandPayload):
    interaction = await grab_interaction(cmd.db, 'sniff')
    target = get_target(pld.msg)
    auth = pld.msg.author
    if not target or target.id == pld.msg.author.id:
        ender = secrets.choice(endings)
        response = discord.Embed(color=0xffcc4d, title=f'👃 {auth.display_name} sniffs {ender}.')
    else:
        response = discord.Embed(color=0xffcc4d, title=f'👃 {auth.display_name} sniffs {target.display_name}.')
    response.set_image(url=interaction['url'])
    response.set_footer(text=await make_footer(cmd, interaction))
    await pld.msg.channel.send(embed=response)
