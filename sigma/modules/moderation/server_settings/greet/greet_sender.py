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
from sigma.core.mechanics.payload import MemberPayload
from sigma.core.utilities.data_processing import movement_message_parser
from sigma.modules.moderation.server_settings.greet.greetmessage import make_greet_embed


async def greet_sender(ev: SigmaEvent, pld: MemberPayload):
    greet_active = pld.settings.get('greet')
    greet_active = True if greet_active is None else greet_active
    if greet_active:
        greet_dm = pld.settings.get('greet_dm')
        if greet_dm:
            target = pld.member
        else:
            greet_channel_id = pld.settings.get('greet_channel')
            target = pld.member.guild.get_channel(greet_channel_id) if greet_channel_id else None
        if target:
            current_greeting = pld.settings.get('greet_message')
            if not current_greeting:
                current_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            greeting_text = movement_message_parser(pld.member, current_greeting)
            greet_embed = pld.settings.get('greet_embed') or {}
            if greet_embed.get('active'):
                greeting = await make_greet_embed(greet_embed, greeting_text, pld.member.guild)
                await target.send(embed=greeting)
            else:
                await target.send(greeting_text)
