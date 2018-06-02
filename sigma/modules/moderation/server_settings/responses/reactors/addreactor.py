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


async def addreactor(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) == 2:
                trigger = args[0].lower()
                if '.' not in trigger:
                    reaction = args[1].replace('<', '').replace('>', '')
                    react_triggers = await cmd.db.get_guild_settings(message.guild.id, 'ReactorTriggers') or {}
                    if trigger in react_triggers:
                        res_text = 'updated'
                    else:
                        res_text = 'added'
                    react_triggers.update({trigger: reaction})
                    await cmd.db.set_guild_settings(message.guild.id, 'ReactorTriggers', react_triggers)
                    response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
                else:
                    response = discord.Embed(title='❗ The trigger can\'t have a dot in it.', color=0xBE1931)
            else:
                response = discord.Embed(title='❗ Invalid number of arguments.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
