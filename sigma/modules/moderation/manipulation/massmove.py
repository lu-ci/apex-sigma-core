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


def get_vc(guild_vcs, lookup):
    """

    :param guild_vcs:
    :type guild_vcs:
    :param lookup:
    :type lookup:
    :return:
    :rtype:
    """
    if lookup.isdigit():
        vc = discord.utils.find(lambda x: x.id == int(lookup), guild_vcs)
    else:
        vc = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), guild_vcs)
    return vc


async def massmove(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            movereqs = [piece.strip() for piece in ' '.join(pld.args).split(';')]
            if len(movereqs) == 2:
                lookup_one = movereqs[0]
                lookup_two = movereqs[1]
                guild_vcs = pld.msg.guild.voice_channels
                vc_one = get_vc(guild_vcs, lookup_one)
                vc_two = get_vc(guild_vcs, lookup_two)
                if vc_one and vc_two:
                    me = pld.msg.guild.me
                    if me.permissions_in(vc_one).mute_members and me.permissions_in(vc_two).mute_members:
                        membs_one = [vcm for vcm in vc_one.members if not vcm.bot]
                        for member in membs_one:
                            await member.move_to(vc_two)
                        response = ok(f'Moved {len(membs_one)} members to {vc_two.name}.')
                    else:
                        response = error('I\'m not permitted to move members.')
                else:
                    response = error('One or both of the channels weren\'t found.')
            else:
                response = error('Invalid arguments. See the usage example.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
