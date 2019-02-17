# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019 Lucia's Cipher
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

import re

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import BanPayload
from sigma.core.sigma import ApexSigma


def get_mod_and_reason(bot: ApexSigma, ban_entry: discord.AuditLogAction, guild: discord.Guild):
    # matches Sigma's Audit reason for bans/kicks
    audit_reason = re.search(r'By (.+)#(\d{4})(: |\.)(.*)', ban_entry.reason or '')
    reason_group = audit_reason.group(4) if audit_reason else None
    reason = reason_group if reason_group else None
    if ban_entry.user.id == bot.user.id:
        try:
            name = audit_reason.group(1).lower()
            udisc = audit_reason.group(2)
            lookup = discord.utils.find(lambda u: u.name.lower() == name and u.discriminator == udisc, guild.members)
        except AttributeError:
            lookup = None
        if lookup:
            mod = lookup
        else:
            mod = ban_entry.user
    else:
        mod = ban_entry.user
    return mod, reason


async def ban_incident_scanner(ev: SigmaCommand, pld: BanPayload):
    ban_entry = None
    now = arrow.utcnow().float_timestamp
    async for ali in pld.guild.audit_logs(limit=100, action=discord.AuditLogAction.ban):
        if ali.target.id == pld.user.id:
            kick_stamp = arrow.get(ali.created_at).float_timestamp
            if now - kick_stamp <= 5:
                ban_entry = ali
    if ban_entry:
        mod, reason = get_mod_and_reason(ev.bot, ban_entry, pld.guild)
        icore = get_incident_core(ev.db)
        incident = icore.generate('ban')
        incident.set_location(pld.guild)
        incident.set_moderator(mod)
        incident.set_target(ban_entry.target)
        if reason:
            incident.set_reason(reason)
        await icore.save(incident)
        incident_embed = incident.to_embed('🔨', 0x993300)
        await icore.report(pld.guild, incident_embed)
