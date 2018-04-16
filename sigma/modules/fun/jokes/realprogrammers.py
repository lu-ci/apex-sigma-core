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

import secrets

import discord
import yaml

from sigma.core.mechanics.command import SigmaCommand

joke_cache = None


async def realprogrammers(cmd: SigmaCommand, message: discord.Message, args: list):
    global joke_cache
    if not joke_cache:
        with open(cmd.resource('real-programmers'), 'r', encoding='utf-8') as joke_file:
            joke_cache = yaml.safe_load(joke_file)
    joke = secrets.choice(joke_cache)
    response = discord.Embed(color=0xf9f9f9, title=f'💻 Real programmers...')
    response.description = joke
    await message.channel.send(embed=response)
