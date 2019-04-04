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

import secrets

import discord

from sigma.modules.interactions.mech.interaction_mechanics import get_author, get_target, grab_interaction, make_footer

endings = ['themself', 'something off the table', 'panties', 'glue', ]


async def sniff(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    interaction = await grab_interaction(cmd.db, 'sniff')
    target, auth = get_target(pld.msg.guild.me, pld.msg), get_author(pld.msg.guild.me, pld.msg)
    noun = secrets.choice(endings)
    ender = f'sniffs {noun}' if target.id == pld.msg.author.id else f'dances with {target.display_name}'
    response = discord.Embed(color=0xffcc4d, title=f'👃 {auth.display_name} {ender}.')
    response.set_image(url=interaction['url'])
    response.set_footer(text=await make_footer(cmd, interaction))
    await pld.msg.channel.send(embed=response)
