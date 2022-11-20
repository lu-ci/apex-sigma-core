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

from sigma.core.utilities.generic_responses import GenericResponse


async def prefix(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    current_prefix = cmd.db.get_prefix(pld.settings)
    if pld.args:
        if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
            new_prefix = ''.join(pld.args)
            if new_prefix != current_prefix:
                prefix_text = new_prefix
                if new_prefix == cmd.bot.cfg.pref.prefix:
                    new_prefix = None
                    prefix_text = cmd.bot.cfg.pref.prefix
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'prefix', new_prefix)
                response = GenericResponse(f'**{prefix_text}** has been set as the new prefix.').ok()
            else:
                response = GenericResponse('The current prefix and the new one are the same.').error()
        else:
            response = GenericResponse('Access Denied. Manage Server needed.').denied()
    else:
        response = GenericResponse(f'**{current_prefix}** is the current prefix.').info()
    await pld.msg.channel.send(embed=response)
