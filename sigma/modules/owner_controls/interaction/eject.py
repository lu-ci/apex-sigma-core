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


async def eject(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        try:
            target = cmd.bot.get_guild(int(''.join(args)))
            if target:
                await target.leave()
                response = discord.Embed(color=0x77B255, title=f'✅ Ejected from {target.name}.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        except ValueError:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing guild ID.')
    await message.channel.send(embed=response)
