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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate


accepted_states = ['dnd', 'idle', 'offline', 'online']


async def inrole(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0].lower()
        role_search = discord.utils.find(lambda x: x.name.lower() == lookup, message.guild.roles)
        if role_search:
            state = None
            members = []
            if len(args) > 1:
                if args[1].startswith('--'):
                    state_name = args[1][2:].lower()
                    if state_name in accepted_states:
                        state = state_name
            for member in message.guild.members:
                if role_search in member.roles:
                    if state:
                        if member.status.name == state:
                            members.append([member.name, member.top_role.name])
                    else:
                        members.append([member.name, member.top_role.name])
            if members:
                page = args[-1] if len(args) > 1 and args[-1].isdigit() else 1
                members, page = paginate(sorted(members), page)
                response = discord.Embed(color=role_search.color)
                total_members = message.guild.member_count
                value = f'```py\n{len(members)} of {total_members} have the {role_search.name} role. Page {page}\n```'
                headers = ['Name', 'Top Role']
                members_table = boop(members, headers)
                response.add_field(name='📄 Details', value=value, inline=False)
                response.add_field(name='👥 Members', value=f'```hs\n{members_table}\n```', inline=False)
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 No users have the {role_search.name} role.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup} not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
