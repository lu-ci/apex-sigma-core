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

import arrow
import discord

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.generic_responses import GenericResponse


async def listinactivewarnings(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author == pld.msg.guild.owner:
        target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
        if target:
            lookup = {'guild': pld.msg.guild.id, 'target.id': target.id, 'warning.active': False}
            warnings = await cmd.db[cmd.db.db_nam].Warnings.find(lookup).to_list(None)
            if warnings:
                warn_list = []
                for warning in warnings:
                    warn_id = warning.get('warning').get('id')
                    moderator = await cmd.bot.get_user(warning.get('moderator').get('id'))
                    if moderator:
                        moderator = moderator.name
                    else:
                        moderator = warning.get('moderator').get('name')
                    warn_time = arrow.get(warning.get('warning').get('timestamp')).format('DD. MMM. YYYY. HH:mm')
                    warn_list.append(f'`{warn_id}` by **{moderator}** on {warn_time}.')
                page = pld.args[1] if len(pld.args) > 1 else 1
                warn_list, page = PaginatorCore.paginate(warn_list, page, 5)
                start_range, end_range = (page - 1) * 5, page * 5
                warn_list = '\n'.join(warn_list)
                ender = 's' if len(warnings) > 1 else ''
                start = f'{target.name} has' if target.id != pld.msg.author.id else 'You have'
                response = discord.Embed(color=0xFFCC4D)
                response.add_field(name=f'⚠ {start} {len(warnings)} inactive warning{ender}.', value=warn_list)
                response.set_footer(text=f'Showing warns {start_range}-{end_range} out of {len(warnings)}.')
            else:
                start = f'{target.name} doesn\'t' if target.id != pld.msg.author.id else 'You don\'t'
                response = discord.Embed(color=0x55acee, title=f'💠 {start} have any inactive warnings.')
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Server Owner needed.').denied()
    await pld.msg.channel.send(embed=response)
