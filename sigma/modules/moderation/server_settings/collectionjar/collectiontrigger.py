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

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def collectiontrigger(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        jar_doc = pld.settings.get('collection_jar') or {}
        if pld.args:
            if len(pld.args) == 1:
                trigger = pld.args[0].lower()
                jar_doc.update({'trigger': trigger})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'collection_jar', jar_doc)
                response = GenericResponse(f'Collection Jar trigger set to `{trigger}`.').ok()
            else:
                response = GenericResponse('Trigger can\'t be more than one word.').error()
        else:
            trigger = jar_doc.get('trigger')
            if trigger:
                response = discord.Embed(color=0xbdddf4, title=f'💬 The current trigger is `{trigger}`.')
            else:
                response = GenericResponse('A trigger has not been set.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
