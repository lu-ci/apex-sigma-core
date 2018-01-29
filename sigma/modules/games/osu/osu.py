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
from lxml import html

osu_logo = 'http://w.ppy.sh/c/c9/Logo.png'


async def osu(cmd, message, args):
    if args:
        osu_input = '%20'.join(args)
        try:
            profile_url = 'https://osu.ppy.sh/u/' + osu_input
            async with aiohttp.ClientSession() as session:
                async with session.get(profile_url) as data:
                    page = await data.text()
            root = html.fromstring(page)
            username = root.cssselect('.profile-username')[0].text[:-1]
            user_color = str(message.author.color)[1:]
            sig_url = f'https://lemmmy.pw/osusig/sig.php?colour=hex{user_color}&uname={osu_input}'
            response = discord.Embed(color=message.author.color)
            response.set_image(url=sig_url)
            response.set_author(name=f'{username}\'s osu! Profile', url=profile_url, icon_url=osu_logo)
        except IndexError:
            response = discord.Embed(color=0xBE1931, title='❗ Unable to retrieve profile.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(None, embed=response)
