# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import ftfy


async def pun(cmd, message, args):
    pun_url = 'http://www.punoftheday.com/cgi-bin/arandompun.pl'
    async with aiohttp.ClientSession() as session:
        async with session.get(pun_url) as data:
            pun_req = await data.text()
    pun_text = pun_req.split('&quot;')[1]
    pun_text = ftfy.fix_text(pun_text)
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😒 Have A Pun', value=pun_text)
    await message.channel.send(None, embed=embed)
