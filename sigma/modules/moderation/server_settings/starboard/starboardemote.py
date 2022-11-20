"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from unicodedata import category

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def starboardemote(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        starboard_doc = pld.settings.get('starboard') or {}
        if pld.args:
            new_emote = pld.args[0][0]
            if category(new_emote) == 'So':
                starboard_doc.update({'emote': new_emote})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'starboard', starboard_doc)
                response = GenericResponse(f'Starboard emote set to {new_emote}').ok()
            else:
                response = GenericResponse('Emote must be native to Discord.').error()
        else:
            emote = starboard_doc.get('emote')
            if emote:
                response = discord.Embed(color=0xFFAC33, title=f'🌟 The current emote is {emote}')
            else:
                response = GenericResponse('An emote has not been set.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
