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

from sigma.core.utilities.generic_responses import denied, error, ok


async def unbindinvite(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.create_instant_invite:
        if pld.args:
            invite_id = pld.args[0]
            forced = pld.args[-1] == ':f'
            invites = await pld.msg.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_id.lower(), invites)
            if target_inv or forced:
                if forced:
                    inv_id = invite_id
                else:
                    inv_id = target_inv.id
                bindings = pld.settings.get('bound_invites')
                if bindings is None:
                    bindings = {}
                if inv_id in bindings:
                    bindings.pop(inv_id)
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'bound_invites', bindings)
                    response = ok(f'Invite {inv_id} has been unbound.')
                else:
                    response = error(f'Invite {inv_id} not bound.')
            else:
                response = error('No invite with that ID was found.')
        else:
            response = error('Not enough arguments. Invite and role name needed.')
    else:
        response = denied('Access Denied. Create Instant Invites needed.')
    await pld.msg.channel.send(embed=response)
