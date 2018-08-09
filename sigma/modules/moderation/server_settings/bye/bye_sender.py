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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import movement_message_parser
from sigma.modules.moderation.server_settings.bye.byemessage import make_bye_embed


async def bye_sender(ev: SigmaEvent, member):
    bye_active = await ev.db.get_guild_settings(member.guild.id, 'bye') or True
    if bye_active:
        bye_channel_id = await ev.db.get_guild_settings(member.guild.id, 'bye_channel')
        if bye_channel_id:
            target = discord.utils.find(lambda x: x.id == bye_channel_id, member.guild.channels)
        else:
            target = None
        if target:
            current_goodbye = await ev.db.get_guild_settings(member.guild.id, 'bye_message')
            if not current_goodbye:
                current_goodbye = '{user_name} has left {server_name}.'
            goodbye_text = movement_message_parser(member, current_goodbye)
            bye_embed = await ev.db.get_guild_settings(member.guild.id, 'bye_embed') or {}
            if bye_embed.get('active'):
                goodbye = await make_bye_embed(bye_embed, goodbye_text, member.guild)
                await target.send(embed=goodbye)
            else:
                await target.send(goodbye_text)
