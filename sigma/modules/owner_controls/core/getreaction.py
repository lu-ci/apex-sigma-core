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


async def getreaction(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        return

    react_id = args[0].lower()
    react_item = await cmd.db[cmd.db.db_cfg.database].Interactions.find_one({'ReactionID': react_id})
    if not react_item:
        return

    response = discord.Embed(color=0x5dadec)
    response.set_image(url=react_item['URL'])
    response.set_footer(text=f'Reaction ID: {react_id}')
    await message.channel.send(embed=response)
