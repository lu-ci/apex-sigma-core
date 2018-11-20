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


def get_vc(guild_vcs, lookup):
    if lookup.isdigit():
        vc = discord.utils.find(lambda x: x.id == int(lookup), guild_vcs)
    else:
        vc = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), guild_vcs)
    return vc


async def massmove(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            movereqs = [piece.strip() for piece in ' '.join(pld.args).split(';')]
            if len(movereqs) == 2:
                guild_vcs = [vc for vc in pld.msg.guild.channels if isinstance(vc, discord.VoiceChannel)]
                lookup_one = movereqs[0]
                lookup_two = movereqs[1]
                vc_one = get_vc(guild_vcs, lookup_one)
                vc_two = get_vc(guild_vcs, lookup_two)
                if vc_one and vc_two:
                    me = pld.msg.guild.me
                    if me.permissions_in(vc_one).mute_members and me.permissions_in(vc_two).mute_members:
                        membs_one = [vcm for vcm in vc_one.members if not vcm.bot]
                        for member in membs_one:
                            await member.move_to(vc_two)
                        move_title = f'✅ Moved {len(membs_one)} members to {vc_two.name}.'
                        response = discord.Embed(color=0x66CC66, title=move_title)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ I\'m not permitted to move members.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ One or both of the channels weren\'t found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid arguments. See the usage example.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)
