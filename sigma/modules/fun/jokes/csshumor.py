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

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def csshumor(_cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    url = 'https://csshumor.com/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.text()
    root = html.fromstring(data)
    codeblock = root.cssselect('.crayon-code')[0]
    codeblock_content = codeblock.text_content()
    await message.channel.send(f'```css\n{codeblock_content}\n```')
