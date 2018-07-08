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

from sigma.core.mechanics.command import SigmaCommand

joke_cache = []


async def joke(cmd: SigmaCommand, message: discord.Message, args: list):
    global joke_cache
    if not joke_cache:
        joke_cache = await cmd.db[cmd.db.db_nam].JokeData.find().to_list(None)
    joke_data = joke_cache.pop(secrets.randbelow(len(joke_cache)))
    joke_text = joke_data.get('body')
    response = discord.Embed(color=0xFFDC5D)
    response.add_field(name='😆 Have A Random Joke', value=joke_text)
    await message.channel.send(embed=response)
