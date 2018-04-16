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


async def geterror(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        token = args[0]
        error_file = await cmd.db[cmd.bot.cfg.db.database].Errors.find_one({'Token': token})
        if error_file:
            response = discord.Embed(color=0xBE1931, title=f'🚨 Error: `{token}`')
            cmd_text = f'Command: **{error_file["Message"]["Command"]}**'
            cmd_text += f'\nID: **{error_file["Message"]["ID"]}**'
            cmd_text += f'\nArguments: **{" ".join(error_file["Message"]["Arguments"]) or "None"}**'
            orgn_text = f'Author: **{error_file["Author"]["Name"]}**'
            orgn_text += f'\nAuthor ID: **{error_file["Author"]["ID"]}**'
            orgn_text += f'\nChannel: **{error_file["Channel"]["Name"]}**'
            orgn_text += f'\nChannel ID: **{error_file["Channel"]["ID"]}**'
            orgn_text += f'\nGuild: **{error_file["Guild"]["Name"]}**'
            orgn_text += f'\nGuild ID: **{error_file["Guild"]["ID"]}**'
            trace_text = f'Trace Class:\n**{error_file["TraceBack"]["Class"]}**'
            trace_text += f'\nTrace Details:\n```py\n{error_file["TraceBack"]["Details"]}\n```'
            response.add_field(name='Command', value=cmd_text)
            response.add_field(name='Origin', value=orgn_text)
        else:
            trace_text = None
            response = discord.Embed(color=0xBE1931, title='❗ No error with that token was found.')
    else:
        trace_text = None
        response = discord.Embed(color=0xBE1931, title='❗ No token inputted.')
    await message.channel.send(embed=response)
    if trace_text:
        await message.channel.send(trace_text)
