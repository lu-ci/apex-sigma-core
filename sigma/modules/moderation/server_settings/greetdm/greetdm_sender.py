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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import movement_message_parser
from sigma.modules.moderation.server_settings.greet.greetmessage import make_greet_embed


async def greetdm_sender(ev: SigmaEvent, member):
    greet_dm_active = await ev.db.get_guild_settings(member.guild.id, 'greet_dm')
    if greet_dm_active:
        if member:
            current_dm_greeting = await ev.db.get_guild_settings(member.guild.id, 'greet_dm_message')
            if not current_dm_greeting:
                current_dm_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            greeting_dm_text = movement_message_parser(member, current_dm_greeting)
            greet_dm_embed = await ev.db.get_guild_settings(member.guild.id, 'greet_dm_embed') or {}
            if greet_dm_embed.get('active'):
                greeting_dm = await make_greet_embed(greet_dm_embed, greeting_dm_text, member.guild)
                await member.send(embed=greeting_dm)
            else:
                await member.send(greeting_dm_text)
