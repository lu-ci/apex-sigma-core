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
import aiohttp
import json
import ftfy
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def randomactivity(_cmd: SigmaCommand, pld: CommandPayload):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://kylebob.com/get.php?category=&search=') as q_req:
            q_page = await q_req.read()
            data = json.loads(q_page)
    todo = ftfy.fix_encoding(data.get('thing'))
    response = discord.Embed(color=0xF9F9F9, title=f'💡 {todo}')
    await pld.msg.channel.send(embed=response)
