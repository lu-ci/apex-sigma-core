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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied


async def activatewarning(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author == message.guild.owner:
        if message.mentions:
            if len(args) == 2:
                target = message.mentions[0]
                warn_id = args[1].lower()
                lookup = {
                    'guild': message.guild.id,
                    'target.id': target.id,
                    'warning.id': warn_id,
                    'warning.active': False
                }
                warn_data = await cmd.db[cmd.db.db_nam].Warnings.find_one(lookup)
                if warn_data:
                    warn_iden = warn_data.get('warning').get('id')
                    change_data = {'$set': {'warning.active': True}}
                    await cmd.db[cmd.db.db_nam].Warnings.update_one(lookup, change_data)
                    response = discord.Embed(color=0x77B255, title=f'✅ Warning {warn_iden} reactivated.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 Inactive warning not found.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Both user tag and warning ID are needed.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ No user targeted.')
    else:
        response = permission_denied('Server Owner')
    await message.channel.send(embed=response)
