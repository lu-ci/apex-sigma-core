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


async def byemessage(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = permission_denied('Manage Server')
    else:
        if args:
            goodbye_text = ' '.join(args)
            await cmd.db.set_guild_settings(message.guild.id, 'ByeMessage', goodbye_text)
            response = discord.Embed(color=0x77B255, title='✅ New Goodbye Message set.')
        else:
            current_goodbye = await cmd.db.get_guild_settings(message.guild.id, 'ByeMessage')
            if current_goodbye is None:
                current_goodbye = '{user_name} has left {server_name}.'
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name='ℹ Current Goodbye Message', value=f'```\n{current_goodbye}\n```')
    await message.channel.send(embed=response)
