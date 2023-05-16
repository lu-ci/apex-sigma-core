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

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse


async def oserverbots(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        lookup = ' '.join(pld.args)
        try:
            gld = await cmd.bot.get_guild(int(lookup))
        except ValueError:
            gld = discord.utils.find(lambda u: u.name.lower() == lookup.lower(), cmd.bot.guilds)
        if gld:
            online_bots, offline_bots = [], []
            total_bots = len([u for u in gld.members if u.bot])
            for user in gld.members:
                if user.bot:
                    name = f'{user.name}#{user.discriminator}'
                    offline_bots.append(name) if str(user.status) == 'offline' else online_bots.append(name)
            if total_bots == 0:
                response = GenericResponse('No bots were found on that server.').error()
            else:
                guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon else None
                response = discord.Embed(color=await get_image_colors(guild_icon))
                response.set_author(name=f'Bots on {gld.name}', icon_url=guild_icon)
                response.add_field(name='Online', value='\n- ' + '\n- '.join(sorted(online_bots)))
                response.add_field(name='Offline', value='\n- ' + '\n- '.join(sorted(offline_bots) or ['None']))
        else:
            response = GenericResponse('Guild not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
