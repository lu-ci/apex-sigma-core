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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found


async def getinteraction(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        react_id = pld.args[0].lower()
        react_item = await cmd.db[cmd.db.db_nam].Interactions.find_one({'interaction_id': react_id})
        if react_item:
            response = discord.Embed(color=0x5dadec)
            response.set_image(url=react_item['url'])
            response.set_footer(text=f'Reaction ID: {react_id}')
        else:
            response = not_found('Reaction not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
