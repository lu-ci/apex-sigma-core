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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def randombetween(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) == 2:
            try:
                min_num = int(pld.args[0])
                max_num = int(pld.args[1])
            except ValueError:
                min_num = None
                max_num = None
            if min_num and max_num:
                if max_num > min_num:
                    ran_num = secrets.randbelow(max_num - min_num)
                    out_num = min_num + ran_num
                    response = discord.Embed(color=0xea596e, title=f'🎲 {out_num}')
                else:
                    response = error('The high number is smaller than the minimum.')
            else:
                response = error('Invalid numbers.')
        else:
            response = error('Invalid number of arguments.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
