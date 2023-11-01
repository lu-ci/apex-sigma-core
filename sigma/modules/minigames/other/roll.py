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

import re
import secrets

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def roll(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    rolls = []

    if not pld.args:
        result = secrets.randbelow(20) + 1
        rolls.append(result)

    elif (die := pld.args[0]).isdigit():
        result = secrets.randbelow(int(die)) + 1
        rolls.append(result)

    elif 'd' in (dice := pld.args[0].lower()):
        ops = {'-': int.__sub__, '+': int.__add__}

        match = re.match(r'(\d+)[Dd](\d+)(?:([-+])(\d+))?', dice)
        count = match.group(1)
        value = match.group(2)
        op = match.group(3) or '+'
        mod = match.group(4) or '0'

        if all([count.isdigit(), value.isdigit(), mod.isdigit()]):
            for _ in range(int(count)):
                result = secrets.randbelow(int(value)) + 1
                result = ops[op](result, int(mod))
                rolls.append(result)

    if rolls:
        response = discord.Embed(color=0xEA596E)
        if len(rolls) <= 20:
            text = ''
            for i, num in enumerate(rolls):
                text += f'\n{i + 1}: **{num}**'
        else:
            text = ', '.join([str(r) for r in rolls])
        response.add_field(name='🎲 Rolls', value=text)
        response.set_footer(text=f'Total: {sum(rolls)}')
    else:
        response = GenericResponse('Invalid roll, please follow the example.').error()

    await pld.msg.channel.send(embed=response)
