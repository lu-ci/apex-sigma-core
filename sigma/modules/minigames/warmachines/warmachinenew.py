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
from sigma.core.mechanics.database import Database
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine

price = 450
resource_names = ['metal', 'biomass', 'ammunition', 'sumarum', 'currency']


async def check_resources(db: Database, uid: int):
    missing = []
    # for res in enumerate(resource_names):
    #     user_res = await db.get_resource(uid, res)
    #     if user_res.current < price:
    #         missing = res
    return missing


async def warmachinenew(cmd: SigmaCommand, message: discord.Message, args: list):
    missing = await check_resources(cmd.db, message.author.id)
    if not missing:
        for res in resource_names:
            await cmd.db.del_resource(message.author.id, res, price, cmd.name, message)
        machine = SigmaMachine(cmd.db, message.author, SigmaMachine.new())
        print(machine.product_name)
        print(machine.stats.health)
        print(SigmaMachine.get_level(3065))
        response = discord.Embed(color=0x8899a6, title=f'🔧 {machine.product_name} constructed.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Not enough {", ".join(missing)}.')
    await message.channel.send(embed=response)
