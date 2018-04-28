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

import json
import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand

joke_cache = []


async def joke(cmd: SigmaCommand, message: discord.Message, args: list):
    if not joke_cache:
        with open(cmd.resource('stupidstuff.json'), 'r', encoding='utf-8') as joke_file:
            jokes = json.loads(joke_file.read())
            [joke_cache.append(joke_item) for joke_item in jokes if len(joke_item.get('body')) < 512]
    joke_data = joke_cache.pop(secrets.randbelow(len(joke_cache)))
    joke_text = joke_data.get('body')
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😆 Have A Random Joke', value=joke_text)
    await message.channel.send(None, embed=embed)
