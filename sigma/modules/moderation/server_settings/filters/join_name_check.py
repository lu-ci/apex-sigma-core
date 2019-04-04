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
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name, is_invalid


async def join_name_check(_ev: SigmaEvent, pld: MemberPayload):
    """

    :param _ev:
    :type _ev:
    :param pld:
    :type pld:
    """
    if pld.member.guild:
        active = pld.settings.get('ascii_only_names')
        if active:
            if is_invalid(pld.member.display_name):
                # noinspection PyBroadException
                try:
                    temp_name = pld.settings.get('ascii_temp_name', '<Change My Name>')
                    new_name = clean_name(pld.member.display_name, temp_name)
                    await pld.member.edit(nick=new_name, reason='ASCII name enforcement.')
                except Exception:
                    pass
