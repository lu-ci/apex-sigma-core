# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018 Lucia's Cipher
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
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine
from sigma.modules.minigames.warmachines.warmachineinspect import find_machine


price = 1


async def warmachinename(cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.args) >= 2:
        lookup = pld.args[0]
        new_name = ' '.join(pld.args[1:])
        machines = await SigmaMachine.get_machines(cmd.db, pld.msg.author)
        machine: SigmaMachine = find_machine(lookup, machines)
        if machine:
            sumarum = await cmd.db.get_resource(pld.msg.author.id, 'sumarum')
            if sumarum.current >= price:
                machine.name = new_name
                await machine.update()
                response = discord.Embed(color=0x77B255, title=f'✅ Machine {machine.id} renamed.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough sumarum.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No warmachine found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    await pld.msg.channel.send(embed=response)
