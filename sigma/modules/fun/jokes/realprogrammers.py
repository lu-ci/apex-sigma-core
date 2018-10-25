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


async def realprogrammers(cmd: SigmaCommand, pld: CommandPayload):
    joke_docs = await cmd.db[cmd.db.db_nam].RealDevsData.find().to_list(None)
    joke = secrets.choice(joke_docs).get('content')
    response = discord.Embed(color=0xf9f9f9, title=f'💻 Real programmers...')
    response.description = joke
    await message.channel.send(embed=response)
