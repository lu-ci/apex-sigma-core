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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import denied, info, ok


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
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            goodbye_text = ' '.join(pld.args)
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'bye_message', goodbye_text)
            response = ok('New Goodbye Message set.')
        else:
            current_goodbye = pld.settings.get('bye_message')
            if not current_goodbye:
                current_goodbye = '{user_name} has left {server_name}.'
            bye_embed = pld.settings.get('bye_embed') or {}
            if bye_embed.get('active'):
                response = await make_bye_embed(bye_embed, current_goodbye, pld.msg.guild)
            else:
                response = info('Current Goodbye Message')
                response.description = current_goodbye
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
