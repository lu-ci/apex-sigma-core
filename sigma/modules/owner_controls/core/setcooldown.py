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


async def setcooldown(cmd: SigmaCommand, message: discord.Message, args: list):
    cooldown = None
    command = None
    if len(args) == 2:
        command = args[0].lower()
        try:
            cooldown = int(args[1])
        except ValueError:
            cooldown = None
    if command and cooldown is not None:
        if command in cmd.bot.modules.alts:
            command = cmd.bot.modules.alts[command]
        if command in cmd.bot.modules.commands.keys():
            await cmd.db[cmd.db.db_cfg.database].CommandCooldowns.insert_one({'Command': command, 'Cooldown': cooldown})
            response = discord.Embed(color=0x66CC66, title=f'✅ Command {command} now has a {cooldown}s cooldown.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Command `{command}` not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No command, or no/invalid cooldown.')
    await message.channel.send(embed=response)
