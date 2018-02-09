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

import hashlib

import discord

from sigma.core.mechanics.command import SigmaCommand


async def makehash(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        embed = discord.Embed(color=0xBE1931, title='❗ No hash inputted and nothing to hash.')
        await message.channel.send(None, embed=embed)
        return
    if len(args) < 2:
        embed = discord.Embed(color=0xBE1931, title='❗ Nothing to hash.')
        await message.channel.send(None, embed=embed)
        return
    hash_name = args[0]
    hashes = hashlib.algorithms_available
    if hash_name not in hashes:
        embed = discord.Embed(color=0xBE1931)
        embed.add_field(name='❗ Unknown Hashing Method',
                        value='Available:\n```\n' + ', '.join(hashes) + '\n```')
        await message.channel.send(None, embed=embed)
        return
    qry = ' '.join(args[1:])
    crypt = hashlib.new(hash_name)
    crypt.update(qry.encode('utf-8'))
    final = crypt.hexdigest()
    embed = discord.Embed(color=0x66cc66)
    embed.add_field(name=f'✅ Hashing With {hash_name.upper()} Done', value=f'```\n{final}\n```')
    await message.channel.send(None, embed=embed)
