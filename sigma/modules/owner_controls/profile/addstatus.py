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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def addstatus(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        status_text = ' '.join(args)
        status_exists = await cmd.db[cmd.db.db_nam].StatusFiles.find_one({'Text': status_text})
        if not status_exists:
            status_id = secrets.token_hex(5)
            status_data = {'Text': status_text, 'ID': status_id}
            await cmd.db[cmd.db.db_nam].StatusFiles.insert_one(status_data)
            response = discord.Embed(color=0x77B255, title=f'✅ Added status `{status_id}`.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Status already exists.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
