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
from sigma.core.utilities.generic_responses import permission_denied


async def prefix(cmd: SigmaCommand, message: discord.Message, args: list):
    current_prefix = await cmd.db.get_prefix(message)
    if args:
        if message.author.permissions_in(message.channel).manage_guild:
            new_prefix = ''.join(args)
            if len(new_prefix) >= 2:
                if new_prefix != current_prefix:
                    prefix_text = new_prefix
                    if new_prefix == cmd.bot.cfg.pref.prefix:
                        new_prefix = None
                        prefix_text = cmd.bot.cfg.pref.prefix
                    await cmd.db.set_guild_settings(message.guild.id, 'prefix', new_prefix)
                    response_title = f'✅ **{prefix_text}** has been set as the new prefix.'
                    response = discord.Embed(color=0x77B255, title=response_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The current prefix and the new one are the same.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The prefix needs to be at least two character.')
        else:
            response = permission_denied('Manage Server')
    else:
        response = discord.Embed(color=0x3B88C3, title=f'ℹ **{current_prefix}** is the current prefix.')
    await message.channel.send(embed=response)
