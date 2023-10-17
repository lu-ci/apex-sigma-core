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

from sigma.core.utilities.generic_responses import GenericResponse


async def getinvites(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        gid = int(pld.args[0])
        guild = await pld.bot.get_guild(gid)
        guild = None
        if guild:
            try:
                invites = await guild.invites()
                error = False
            except discord.Forbidden:
                invites = []
                if guild.me.guild_permissions.create_instant_invite:
                    for channel in guild.channels:
                        if isinstance(channel, discord.TextChannel):
                            try:
                                invites.append(await channel.create_invite())
                                break
                            except discord.Forbidden:
                                pass
                if len(invites) == 0:
                    error = True
                else:
                    error = False
            if not error:
                if len(invites) != 0:
                    response = GenericResponse('Invites found.').ok()
                    response.set_footer(text=f'{guild.name} [{guild.id}]')
                    body = ''
                    for invite in invites[:10]:
                        body += f'\n[{invite.code}]({invite.url})'
                    response.description = body
                else:
                    response = GenericResponse('No invites found.').error()
            else:
                response = GenericResponse('No access to invites.').error()
        else:
            response = GenericResponse('Guild not found, placing request in queue.').error()
            queue_data = {
                'guild': gid,
                'author': pld.msg.author.id,
                'timestamp': arrow.utcnow().int_timestamp,
                'reported': False
            }
            await cmd.db[cmd.db.db_nam].InviteQueue.insert_one(queue_data)
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
