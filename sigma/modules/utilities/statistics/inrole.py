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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.generic_responses import GenericResponse

accepted_states = ['dnd', 'idle', 'offline', 'online']


def parse_args(args):
    """
    :type args: list[str]
    :rtype: str, str, int
    """
    state, page = None, 1
    for _ in range(0, 2):
        if args[-1].startswith('--'):
            state_name = args[-1][2:].lower()
            if state_name in accepted_states:
                state = state_name
                args.pop(-1)
        elif args[-1].isdigit():
            page = int(args[-1])
            args.pop(-1)
    lookup = ' '.join(args).lower()
    return lookup, state, page


async def inrole(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            lookup, state, page = parse_args(pld.args)
        except IndexError:
            response = GenericResponse('Bad input. See usage example.').error()
            await pld.msg.channel.send(embed=response)
            return
        if lookup:
            role_search = discord.utils.find(lambda x: x.name.lower() == lookup, pld.msg.guild.roles)
            if role_search:
                members = []
                for member in pld.msg.guild.members:
                    if role_search in member.roles:
                        if state:
                            if member.status.name == state:
                                members.append([member.name, member.top_role.name])
                        else:
                            members.append([member.name, member.top_role.name])
                if members:
                    count = len(members)
                    members, page = PaginatorCore.paginate(sorted(members), page)
                    response = discord.Embed(color=role_search.color)
                    state = state if state else 'Any'
                    value = f'```py\nShowing 10 of {count} users. Status: {state}. Page {page}\n```'
                    members_table = boop(members, ['Name', 'Top Role'])
                    response.add_field(name='📄 Details', value=value, inline=False)
                    response.add_field(name='👥 Members', value=f'```hs\n{members_table}\n```', inline=False)
                else:
                    response = GenericResponse(f'No users have the {role_search.name} role.').not_found()
            else:
                response = GenericResponse(f'{lookup} not found.').not_found()
        else:
            response = GenericResponse('Missing role name.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
