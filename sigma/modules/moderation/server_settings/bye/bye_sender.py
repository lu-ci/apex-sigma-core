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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MemberPayload
from sigma.core.utilities.data_processing import movement_message_parser
from sigma.modules.moderation.server_settings.bye.byemessage import make_bye_embed


async def bye_sender(_ev, pld: MemberPayload):
    """
    :param _ev: The main event instance referenced.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    :param pld:
    :type pld:
    """
    bye_active = pld.settings.get('bye')
    bye_active = True if bye_active is None else bye_active
    if bye_active:
        bye_channel_id = pld.settings.get('bye_channel')
        target = pld.member.guild.get_channel(bye_channel_id) if bye_channel_id else None
        if target:
            current_goodbye = pld.settings.get('bye_message')
            if not current_goodbye:
                current_goodbye = '{user_name} has left {server_name}.'
            goodbye_text = movement_message_parser(pld.member, current_goodbye)
            bye_embed = pld.settings.get('bye_embed', {})
            if bye_embed.get('active'):
                goodbye = await make_bye_embed(bye_embed, goodbye_text, pld.member.guild)
                await target.send(embed=goodbye)
            else:
                await target.send(goodbye_text)
