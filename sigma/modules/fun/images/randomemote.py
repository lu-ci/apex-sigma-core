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

import secrets

import discord

from sigma.core.utilities.generic_responses import error
from sigma.modules.utilities.images.emote import get_emote_cache


async def randomemote(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    emotes, nsfw = pld.msg.guild.emojis, False
    if pld.args:
        if pld.args[-1].lower() == '--global':
            emotes, nsfw = await get_emote_cache(cmd), True
    if not nsfw or pld.msg.channel.is_nsfw():
        if emotes:
            emote = secrets.choice(emotes)
            response = discord.Embed().set_image(url=emote.url)
        else:
            response = error('This server has no custom emotes.')
    else:
        response = error('Emotes from other servers can be NSFW.')
        response.description = 'Mark this channel as NSFW or move to one that is.'
    await pld.msg.channel.send(embed=response)
