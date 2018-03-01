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


async def bindgreeting(cmd: SigmaCommand, message: discord.Message, args: list):
    await cmd.bot.modules.commands.get('syncinvites').execute(message, ['noresp'])
    if message.author.guild_permissions.manage_guild:
        if len(args) >= 2:
            invite_code = args[0]
            greeting_message = ' '.join(args[1:])
            invites = await message.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_code.lower(), invites)
            if target_inv:
                bound_greetings = await cmd.db.get_guild_settings(message.guild.id, 'BoundGreetings') or {}
                ender = "updated" if target_inv.id in bound_greetings else "added"
                bound_greetings.update({target_inv.id: greeting_message})
                await cmd.db.set_guild_settings(message.guild.id, 'BoundGreetings', bound_greetings)
                response = discord.Embed(color=0x77B255, title=f'✅ Greet binding to {target_inv.id} has been {ender}.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Couldn\'t find that invite.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = permission_denied('Manage Guild')
    await message.channel.send(embed=response)
