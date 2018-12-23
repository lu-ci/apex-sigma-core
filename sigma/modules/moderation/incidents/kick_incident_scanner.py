# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018 Lucia's Cipher
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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import MemberPayload


async def kick_incident_scanner(cmd: SigmaCommand, pld: MemberPayload):
    kick_entry = None
    now = arrow.utcnow().float_timestamp
    async for ali in pld.member.guild.audit_logs(limit=100, action=discord.AuditLogAction.kick):
        if ali.target.id == pld.member.id:
            kick_stamp = arrow.get(ali.created_at).float_timestamp
            if now - kick_stamp <= 5:
                kick_entry = ali
    if kick_entry:
        icore = get_incident_core(cmd.db)
        incident = await icore.generate('kick')
        incident.set_location(pld.member.guild)
        incident.set_moderator(kick_entry.user)
        incident.set_target(kick_entry.target)
        incident.set_reason(kick_entry.reason)
        await icore.save(incident)
        incident_embed = incident.to_embed('👢', 0xc1694f)
        await icore.report(pld.member.guild, incident_embed)
