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


async def wipeinventory(cmd: SigmaCommand, pld: CommandPayload):
    try:
        target = cmd.bot.get_user(int(args[0])) if args else None
    except ValueError:
        target = None
    if target:
        await cmd.db.update_inventory(target.id, [])
        response = discord.Embed(color=0xFFCC4D, title=f'🔥 Ok, I\'ve wiped {target.display_name}\'s inventory.')
    else:
        response = discord.Embed(color=0x696969, title='🔍 User not found.')
    await message.channel.send(embed=response)
