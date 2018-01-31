# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

from sigma.core.utilities.data_processing import movement_message_parser


async def bye_sender(ev, member):
    bye_active = await ev.db.get_guild_settings(member.guild.id, 'Bye')
    if bye_active is True or bye_active is None:
        bye_channel_id = await ev.db.get_guild_settings(member.guild.id, 'ByeChannel')
        if bye_channel_id is None:
            target = None
        else:
            target = discord.utils.find(lambda x: x.id == bye_channel_id, member.guild.channels)
        if target:
            current_goodbye = await ev.db.get_guild_settings(member.guild.id, 'ByeMessage')
            if current_goodbye is None:
                current_goodbye = '{user_name} has left {server_name}.'
            goodbye_text = movement_message_parser(member, current_goodbye)
            await target.send(goodbye_text)
