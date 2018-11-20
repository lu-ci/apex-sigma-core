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


import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def markovchain(cmd: SigmaCommand, pld: CommandPayload):
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    collection = await cmd.db[cmd.db.db_nam].MarkovChains.find_one({'user_id': target.id})
    if collection:
        chain = collection.get('chain')
        starter = 'You have' if target.id == pld.msg.author.id else f'{target.name} has'
        ender = 'your' if target.id == pld.msg.author.id else 'their'
        response = discord.Embed(color=0xF9F9F9, title=f'⛓ {starter} {len(chain)} items in {ender} chain.')
    else:
        starter = 'You don\'t have' if target.id == pld.msg.author.id else f'{target.name} doesn\'t have'
        response = discord.Embed(color=0x696969, title=f'🔍 {starter} a collected chain.')
    await pld.msg.channel.send(embed=response)
