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

from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine


def find_machine(lookup: str, machines: list):
    """

    :param lookup:
    :type lookup:
    :param machines:
    :type machines:
    :return:
    :rtype:
    """
    machine = None
    lookup = lookup.lower()
    for machine_item in machines:
        name_match = machine_item.name.lower() == lookup
        id_match = machine_item.id.lower() == lookup
        prod_name_match = machine_item.product_name.lower() == lookup
        if id_match or name_match or prod_name_match:
            machine = machine_item
            break
    return machine


async def warmachineinspect(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        lookup = ' '.join(pld.args)
        machines = await SigmaMachine.get_machines(cmd.db, pld.msg.author)
        machine: SigmaMachine = find_machine(lookup, machines)
        if machine:
            stats_block = f'**Health**: {machine.stats.health}'
            stats_block += f' | **Damage**: {machine.stats.damage}'
            stats_block += f' | **Accuracy**: {machine.stats.damage}'
            stats_block += f'\n**Evasion**: {machine.stats.damage}'
            stats_block += f' | **Rate of Fire**: {machine.stats.damage}'
            stats_block += f' | **Critical Chance**: {machine.stats.damage}'
            stats_block += f'\n**Critical Multiplier**: {machine.stats.damage}'
            stats_block += f' | **Armor**: {machine.stats.damage}'
            stats_block += f' | **Armor Penetration**: {machine.stats.damage}'
            response = discord.Embed(color=0x3B88C3, title=f'🤖 {machine.id}: {machine.name}')
            response.description = f'**Production**: {machine.product_name}'
            response.add_field(name='Battles', value=f'**Won**: {machine.won} | **Lost**: {machine.lost}', inline=False)
            response.add_field(name='Statistics', value=stats_block, inline=False)
        else:
            response = not_found('No warmachine found.')
    else:
        response = error('Invalid number of arguments.')
    await pld.msg.channel.send(embed=response)
