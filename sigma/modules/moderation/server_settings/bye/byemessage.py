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
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import permission_denied


async def make_bye_embed(data: dict, goodbye: str, guild: discord.Guild):
    guild_color = await get_image_colors(guild.icon_url)
    goodbye = discord.Embed(color=data.get('color') or guild_color, description=goodbye)
    goodbye.set_author(name=guild.name, icon_url=guild.icon_url)
    if data.get('thumbnail'):
        goodbye.set_thumbnail(url=data.get('thumbnail'))
    if data.get('image'):
        goodbye.set_image(url=data.get('image'))
    return goodbye


async def byemessage(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            goodbye_text = ' '.join(args)
            await cmd.db.set_guild_settings(message.guild.id, 'bye_message', goodbye_text)
            response = discord.Embed(color=0x77B255, title='✅ New Goodbye Message set.')
        else:
            current_goodbye = await cmd.db.get_guild_settings(message.guild.id, 'bye_message')
            if not current_goodbye:
                current_goodbye = '{user_name} has left {server_name}.'
            bye_embed = await cmd.db.get_guild_settings(message.guild.id, 'bye_embed') or {}
            if bye_embed.get('active'):
                response = await make_bye_embed(bye_embed, current_goodbye, message.guild)
            else:
                response = discord.Embed(color=0x3B88C3, title='ℹ Current Goodbye Message')
                response.description = current_goodbye
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
