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

import discord

from .mech.danbooru_cache import get_dan_post


async def danbooru(cmd, message, args):
    if not args:
        tag = 'nude'
    else:
        tag = '+'.join(args).lower()
    image_url = await get_dan_post(tag)
    if not image_url:
        response = discord.Embed(color=0x696969, title=f'🔍 Search for {tag} yielded no results.')
        response.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
    else:
        response = discord.Embed(color=0x744EAA)
        response.set_image(url=image_url)
    await message.channel.send(None, embed=response)
