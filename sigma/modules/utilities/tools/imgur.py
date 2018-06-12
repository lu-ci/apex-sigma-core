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
import discord
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from sigma.core.mechanics.command import SigmaCommand


async def imgur(cmd: SigmaCommand, message: discord.Message, args: list):
    if 'client_id' and 'client_secret' in cmd.cfg:
        client = ImgurClient(cmd.cfg['client_id'], cmd.cfg['client_secret'])
        if args or message.attachments:
            image_url = message.attachments[0].url if message.attachments else ' '.join(args)
            try:
                image = client.upload_from_url(image_url, anon=True)
                imgur_icon = 'https://i.imgur.com/SfU0dnX.png'
                response = discord.Embed(color=0x85BF25)
                response.set_author(name=f'{image["link"]}', icon_url=imgur_icon, url=image["link"])
            except ImgurClientError:
                ender = 'Attachment' if message.attachments else 'URL'
                response = discord.Embed(color=0xBE1931, title=f'❗ Bad {ender}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ The API Key is missing.')
    await message.channel.send(embed=response)
