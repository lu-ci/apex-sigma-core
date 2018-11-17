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

from unicodedata import category

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied


async def starboardemote(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        starboard_doc = pld.settings.get('starboard') or {}
        if pld.args:
            new_emote = pld.args[0][0]
            if category(new_emote) == 'So':
                starboard_doc.update({'emote': new_emote})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'starboard', starboard_doc)
                response = discord.Embed(color=0x77B255, title=f'✅ Starboard emote set to {new_emote}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Emote must be native to Discord.')
        else:
            emote = starboard_doc.get('emote')
            if emote:
                response = discord.Embed(color=0xFFAC33, title=f'🌟 The current emote is {emote}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ An emote has not been set.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)
