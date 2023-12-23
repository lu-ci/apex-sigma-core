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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


async def listraffles(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = {'author': pld.msg.author.id, 'active': True}
    raffle_docs = await cmd.db.col.Raffles.find(lookup).to_list(None)
    if raffle_docs:
        raffle_lines = []
        for raf_doc in raffle_docs:
            raffle_channel = await cmd.bot.get_channel(raf_doc.get('channel'))
            if raffle_channel:
                location = f'in **#{raffle_channel.name}** on **{raffle_channel.guild.name}**.'
            else:
                location = 'in an unknown location.'
            hum_time = arrow.get(raf_doc.get('end')).humanize()
            raffle_line = f'`{raf_doc.get("id")}` ends {hum_time} {location}.'
            raffle_lines.append(raffle_line)
        outlist = '\n'.join(raffle_lines)
        response = discord.Embed(color=pld.msg.author.color)
        response.set_author(name=f'{pld.msg.author.name}\'s Raffles', icon_url=user_avatar(pld.msg.author))
        response.description = outlist
    else:
        response = GenericResponse('You have no pending raffles.').not_found()
    await pld.msg.channel.send(embed=response)
