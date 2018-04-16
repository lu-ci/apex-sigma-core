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

from sigma.core.utilities.data_processing import movement_message_parser


async def greet_sender(ev, member):
    greet_active = await ev.db.get_guild_settings(member.guild.id, 'Greet')
    if greet_active is True or greet_active is None:
        greet_dm = await ev.db.get_guild_settings(member.guild.id, 'GreetDM')
        if greet_dm:
            target = member
        else:
            greet_channel_id = await ev.db.get_guild_settings(member.guild.id, 'GreetChannel')
            if greet_channel_id is None:
                target = None
            else:
                target = discord.utils.find(lambda x: x.id == greet_channel_id, member.guild.channels)
        if target:
            current_greeting = await ev.db.get_guild_settings(member.guild.id, 'GreetMessage')
            if current_greeting is None:
                current_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            greeting_text = movement_message_parser(member, current_greeting)
            await target.send(greeting_text)
