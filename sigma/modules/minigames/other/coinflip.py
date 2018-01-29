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
import secrets

import discord


async def coinflip(cmd, message, args):
    result = secrets.choice(['heads', 'tails'])
    urls = {
        'heads': 'https://i.imgur.com/528MDba.png',
        'tails': 'https://i.imgur.com/A42nfrB.png'
    }
    embed = discord.Embed(color=0x1abc9c)
    if args:
        choice = args[0]
        if choice.lower().startswith('t') or choice.lower().startswith('h'):
            if choice.lower().startswith('t'):
                choice = 'tails'
            else:
                choice = 'heads'
            if result == choice.lower():
                out = '☑ Nice guess!'
            else:
                out = '🇽 Better luck next time!'
            embed = discord.Embed(color=0x1abc9c, title=out)
    embed.set_image(url=urls[result])
    await message.channel.send(None, embed=embed)
