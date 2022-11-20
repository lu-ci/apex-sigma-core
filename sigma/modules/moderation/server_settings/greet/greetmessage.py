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


async def make_greet_embed(data, greeting, guild):
    """
    :type data: dict
    :type greeting: str
    :type guild: discord.Guild
    :rtype: discord.Embed
    """
    guild_icon = str(guild.icon_url) if guild.icon_url else discord.Embed.Empty
    guild_color = await get_image_colors(guild_icon)
    greeting = discord.Embed(color=data.get('color') or guild_color, description=greeting)
    greeting.set_author(name=guild.name, icon_url=guild_icon)
    if data.get('thumbnail'):
        greeting.set_thumbnail(url=data.get('thumbnail'))
    if data.get('image'):
        greeting.set_image(url=data.get('image'))
    return greeting


async def greetmessage(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if pld.args:
            greeting_text = ' '.join(pld.args)
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'greet_message', greeting_text)
            response = GenericResponse('New Greeting Message set.').ok()
        else:
            current_greeting = pld.settings.get('greet_message')
            if not current_greeting:
                current_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            greet_embed = pld.settings.get('greet_embed') or {}
            if greet_embed.get('active'):
                response = await make_greet_embed(greet_embed, current_greeting, pld.msg.guild)
            else:
                response = GenericResponse('Current Greeting Message').info()
                response.description = current_greeting
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
