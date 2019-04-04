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

import arrow
import discord

from sigma.core.mechanics.payload import MemberPayload
from sigma.core.utilities.data_processing import get_time_difference, user_avatar
from sigma.core.utilities.event_logging import log_event


async def leave_logger(ev, pld: MemberPayload):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld:
    :type pld:
    """
    member = pld.member
    response = discord.Embed(color=0xBE1931, timestamp=arrow.utcnow().datetime)
    response.set_author(name='A Member Has Left', icon_url=user_avatar(member))
    response.add_field(name='📤 Leaving Member', value=f'{member.mention}\n{member.name}#{member.discriminator}')
    new_acc, diff_msg = get_time_difference(member, leave=True)
    response.add_field(name='🕑 Member Joined', value=f'{diff_msg.title()}')
    response.set_footer(text=f'User ID: {member.id}')
    await log_event(ev.bot, pld.settings, response, 'log_movement')
