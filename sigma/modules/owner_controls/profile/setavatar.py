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

from sigma.core.mechanics.command import SigmaCommand


async def setavatar(cmd: SigmaCommand, pld: CommandPayload):
    if args or message.attachments:
        image_url = message.attachments[0].url if message.attachments else args[0]
        try:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as image_response:
                        img_data = await image_response.read()
                await cmd.bot.user.edit(avatar=img_data)
                response = discord.Embed(color=0x77B255, title='✅ My avatar has been changed.')
            except aiohttp.client_exceptions.InvalidURL:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid URL.')
        except discord.Forbidden:
            response = discord.Embed(color=0xBE1931, title='❗ I was unable to change my avatar.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Give me a link or attach an image, please.')
    await message.channel.send(embed=response)
