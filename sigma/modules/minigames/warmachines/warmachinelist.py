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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine


async def warmachinelist(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    machines = await SigmaMachine.get_machines(cmd.db, target)
    machines_owned = len(machines)
    machines, page = PaginatorCore.paginate(machines, pld.args[0] if pld.args else 1, 5)
    if machines:
        out_list = '\n'.join([f'`{m.id}`: **{m.name}**' for m in machines])
        response = discord.Embed(color=0x8899a6)
        response.set_author(name=f'{target.name}\'s Warmachines', icon_url=user_avatar(target))
        response.add_field(name='List', value=out_list, inline=False)
        response.set_footer(text=f'[Page {page}] Showing {len(machines)}/{machines_owned} machines owned.')
    else:
        response = error('You don\'t own any machine.')
    await pld.msg.channel.send(embed=response)
