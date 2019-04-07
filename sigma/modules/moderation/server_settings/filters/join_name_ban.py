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

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MemberPayload


async def join_name_ban(_ev, pld: MemberPayload):
    """
    :param _ev: The main event instance referenced.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    :param pld:
    :type pld:
    """
    if pld.member.guild:
        active = pld.settings.get('name_filter_ban')
        if active:
            bad_name = None
            blocked_names = pld.settings.get('blocked_names') or []
            for name in blocked_names:
                if name in pld.member.name.lower():
                    bad_name = name
                    break
            if bad_name:
                # noinspection PyBroadException
                try:
                    reason = f'Had "{bad_name}" in their name'
                    to_target = discord.Embed(color=0x696969)
                    to_target.add_field(name='🔨 You have been banned.', value=f'Reason: {reason}')
                    to_target.set_footer(text=f'From: {pld.member.guild.name}.', icon_url=pld.member.guild.icon_url)
                    try:
                        await pld.member.send(embed=to_target)
                    except discord.Forbidden:
                        pass
                    await pld.member.ban(reason=f'Autoban: {reason}.')
                except Exception:
                    pass
