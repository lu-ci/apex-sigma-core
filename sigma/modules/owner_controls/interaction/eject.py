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


async def eject(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        guild_id = ''.join(args)
        try:
            guild_id = int(guild_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == guild_id, cmd.bot.guilds)
            if target:
                await target.leave()
                response = discord.Embed(color=0x77B255, title=f'✅ Ejected from {target.name}.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)
