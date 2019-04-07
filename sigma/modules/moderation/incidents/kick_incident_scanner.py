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

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import MemberPayload
from sigma.modules.moderation.incidents.ban_incident_scanner import get_mod_and_reason


async def kick_incident_scanner(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MemberPayload
    """
    kick_entry = None
    now = arrow.utcnow().float_timestamp
    async for ali in pld.member.guild.audit_logs(limit=100, action=discord.AuditLogAction.kick):
        if ali.target.id == pld.member.id:
            kick_stamp = arrow.get(ali.created_at).float_timestamp
            if now - kick_stamp <= 5:
                kick_entry = ali
    if kick_entry:
        mod, reason = get_mod_and_reason(ev.bot, kick_entry, pld.member.guild)
        icore = get_incident_core(ev.db)
        incident = icore.generate('kick')
        incident.set_location(pld.member.guild)
        incident.set_moderator(mod)
        incident.set_target(kick_entry.target)
        if reason:
            incident.set_reason(reason)
        await icore.save(incident)
        incident_embed = incident.to_embed('👢', 0xc1694f)
        await icore.report(pld.member.guild, incident_embed)
