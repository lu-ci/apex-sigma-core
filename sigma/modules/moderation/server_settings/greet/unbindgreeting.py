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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied


async def unbindgreeting(cmd: SigmaCommand, message: discord.Message, args: list):
    await cmd.bot.modules.commands.get('syncinvites').execute(message, ['noresp'])
    if message.author.guild_permissions.manage_guild:
        if args:
            invite_code = args[0]
            bound_greetings = await cmd.db.get_guild_settings(message.guild.id, 'BoundGreetings') or {}
            if invite_code in bound_greetings:
                bound_greetings.pop(invite_code)
                response = discord.Embed(color=0x77B255, title=f'✅ Greet binding to {invite_code} has been removed.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Couldn\'t find that invite.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing invite code.')
    else:
        response = permission_denied('Manage Guild')
    await message.channel.send(embed=response)
