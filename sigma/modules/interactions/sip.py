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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.interactions.mech.interaction_mechanics import grab_interaction, get_target, make_footer


async def sip(cmd: SigmaCommand, pld: CommandPayload):
    interaction = await grab_interaction(cmd.db, 'sip')
    target = get_target(pld.msg)
    auth = pld.msg.author
    if not target or target.id == pld.msg.author.id:
        response = discord.Embed(color=0xa6d388, title=f'🍵 {auth.display_name} sips their beverage.')
    else:
        response = discord.Embed(
            color=0xa6d388, title=f'🍵 {auth.display_name} takes a sip with {target.display_name}.'
        )
    response.set_image(url=interaction['url'])
    response.set_footer(text=await make_footer(cmd, interaction))
    await pld.msg.channel.send(embed=response)
