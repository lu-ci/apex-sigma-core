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


async def choosemany(_cmd: SigmaCommand, pld: CommandPayload):
    if len(pld.args) >= 2:
        if pld.args[0].isdigit():
            choices = ' '.join(pld.args[1:]).split('; ')
            limit = int(pld.args[0])
            if 0 < limit < len(choices):
                results = []
                for _ in range(limit):
                    choice = choices.pop(secrets.randbelow(len(choices)))
                    results.append(choice)
                response = discord.Embed(color=0x1ABC9C, title=f'🤔 I choose...')
                results = list(map(lambda x: x if len(x) < 25 else x[:25] + '...', results))
                response.description = '\n'.join(results)
            else:
                response = error('Limit must be lower than the number of choices.')
        else:
            response = error('Limit must be a number.')
    else:
        response = error('Invalid number of arguments.')
    await pld.msg.channel.send(embed=response)
