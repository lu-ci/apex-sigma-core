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

import aiohttp
import discord
import lxml.html as lx

from sigma.core.utilities.generic_responses import error


def split_content(text):
    """
    :param text: The text_content() of the pun block.
    :type text: str
    :rtype: str
    """
    right = text.split('#')[-1]
    while right[0].isdigit():
        right = right[1:]
    if right[-1] not in ['.', '?', '!']:
        right += '.'
    return right


async def pun(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    pun_url = 'https://pun.me/random/'
    async with aiohttp.ClientSession() as session:
        async with session.get(pun_url) as data:
            pun_req = await data.text()
    root = lx.fromstring(pun_req)
    pun_li = root.cssselect('.puns.single li')[0]
    pun_text = split_content(pun_li.text_content())
    if pun_text:
        response = discord.Embed(color=0xFFDC5D, title='😒 Have a pun...')
        response.description = pun_text
    else:
        response = error('Sorry, I failed to find a pun.')
    await pld.msg.channel.send(embed=response)
