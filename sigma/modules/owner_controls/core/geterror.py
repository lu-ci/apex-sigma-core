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
from sigma.core.mechanics.errors import make_error_embed


async def geterror(cmd: SigmaCommand, message: discord.Message, args: list):
    trace_text = None
    if args:
        token = args[0]
        error_file = await cmd.db[cmd.bot.cfg.db.database].Errors.find_one({'token': token})
        if error_file:
            response, trace_text = make_error_embed(error_file)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No error with that token was found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing error token.')
    await message.channel.send(embed=response)
    if trace_text:
        await message.channel.send(trace_text)
