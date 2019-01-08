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
from sigma.core.utilities.generic_responses import denied


async def starboardlimit(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            try:
                new_limit = abs(int(pld.args[0]))
            except ValueError:
                new_limit = None
            if new_limit is not None:
                starboard_doc = pld.settings.get('starboard') or {}
                starboard_doc.update({'limit': int(new_limit)})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'starboard', starboard_doc)
                response = discord.Embed(color=0x77B255, title=f'✅ Starboard limit set to {new_limit}.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Limit must be a number.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)
