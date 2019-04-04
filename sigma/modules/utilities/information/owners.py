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


async def owners(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    owner_lines = []
    for owner in cmd.bot.cfg.dsc.owners:
        member = await cmd.bot.get_user(owner)
        if member:
            owner_line = f'{member.name}#{member.discriminator}'
        else:
            owner_line = f'{owner}'
        owner_lines.append(owner_line)
    owner_list = '\n'.join(owner_lines)
    response = discord.Embed(color=0x1B6F5F)
    response.add_field(name='Owner List', value=owner_list)
    await pld.msg.channel.send(embed=response)
