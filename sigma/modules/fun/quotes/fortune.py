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

import os
import secrets

import discord

fortune_files = []


async def fortune(cmd, message, args):
    if not fortune_files:
        for fortune_file in os.listdir(cmd.resource('fortune')):
            with open(cmd.resource(f'fortune/{fortune_file}')) as forfile:
                text_data = forfile.read()
                fortune_files.append(text_data.split('%'))
    category = secrets.choice(fortune_files)
    fort = None
    while fort is None or len(fort) > 800:
        fort = secrets.choice(category)
    response = discord.Embed(color=0x8CCAF7)
    response.add_field(name='🔮 Fortune', value=fort)
    await message.channel.send(embed=response)
