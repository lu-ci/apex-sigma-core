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


async def resetserver(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.id == pld.msg.guild.owner.id:
        settings, perms, valid = True, True, True
        perms_coll = cmd.db[cmd.db.db_nam].Permissions
        settings_coll = cmd.db[cmd.db.db_nam].ServerSettings
        if pld.args:
            if pld.args[-1].lower() == '--permsonly':
                settings = False
            elif pld.args[-1].lower() == '--settingsonly':
                perms = False
            else:
                valid = False
        if valid:
            if perms:
                await perms_coll.delete_one({'server_id': pld.msg.guild.id})
            if settings:
                await settings_coll.delete_one({'server_id': pld.msg.guild.id})
            title = f'Wiped all server {"permissions" if perms else ""}'
            title += " and " if perms and settings else ""
            title += 'settings' if settings else ''
            response = discord.Embed(color=0x66CC66, title=f'✅ {title}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid arguments, see usage example.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Settings can only be reset by the server owner.')
    await pld.msg.channel.send(embed=response)
