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


async def addcommand(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 2:
                trigger = args[0].lower()
                if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                    content = ' '.join(args[1:])
                    custom_commands = await cmd.db.get_guild_settings(message.guild.id, 'CustomCommands') or {}
                    if trigger in custom_commands:
                        res_text = 'updated'
                    else:
                        res_text = 'added'
                    custom_commands.update({trigger: content})
                    await cmd.db.set_guild_settings(message.guild.id, 'CustomCommands', custom_commands)
                    response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
                else:
                    response = discord.Embed(title='❗ Can\'t replace an existing core command', color=0xBE1931)
            else:
                response = discord.Embed(title='❗ Invalid number of arguments.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
