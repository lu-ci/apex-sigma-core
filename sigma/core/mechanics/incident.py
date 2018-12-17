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

import secrets

import arrow
import discord

from sigma.core.mechanics.database import Database


incident_core_cache = None


def get_incident_core(db: Database):
    global incident_core_cache
    if incident_core_cache is None:
        incident_core_cache = IncidentCore(db)
    return incident_core_cache


class IncidentUser(object):
    def __init__(self, entity: dict or discord.Member = None):
        self.entity = entity
        if isinstance(entity, dict):
            self.from_dict(entity)
        elif isinstance(entity, discord.Member):
            self.from_user(entity)
        else:
            self.id = None
            self.name = None
            self.discriminator = None

    def from_user(self, user: discord.Member):
        self.id = user.id
        self.name = user.name
        self.discriminator = user.discriminator

    def from_dict(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name')
        self.discriminator = data.get('discriminator')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'discriminator': self.discriminator}


class IncidentLocation(object):
    def __init__(self, entity: dict or discord.TextChannel or discord.Guild = None):
        self.entity = entity
        if isinstance(entity, dict):
            self.from_dict(entity)
        elif isinstance(entity, discord.TextChannel) or isinstance(entity, discord.Guild):
            self.from_obj(entity)
        else:
            self.id = None
            self.name = None

    def from_obj(self, obj: discord.TextChannel or discord.Guild):
        self.id = obj.id
        self.name = obj.name

    def from_dict(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name')

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Incident(object):
    def __init__(self, data: dict = None):
        self.data = data if data is not None else {}
        self.id = self.data.get('id')
        self.variant = self.data.get('variant')
        self.moderator = IncidentUser(self.data.get('moderator'))
        self.target = IncidentUser(self.data.get('target'))
        self.channel = IncidentLocation(self.data.get('channel'))
        self.guild = IncidentLocation(self.data.get('guild'))
        self.reason = self.data.get('reason')
        self.edits = self.data.get('edits', [])

    def set_moderator(self, user: discord.Member):
        self.moderator = IncidentUser(user)

    def set_target(self, user: discord.Member):
        self.target = IncidentUser(user)

    def set_location(self, channel: discord.TextChannel):
        self.channel = IncidentLocation(channel)
        self.guild = IncidentLocation(channel.guild)

    def set_reason(self, text: str):
        self.reason = text

    def edit(self, user: discord.Member, reason: str):
        previous = self.to_dict()
        self.reason = reason
        by = IncidentUser(user)
        when = arrow.utcnow().float_timestamp
        self.edits.append({'moderator': by.to_dict(), 'timestamp': when, 'previous': previous})

    def to_dict(self):
        return {
            'id': self.id, 'variant': self.variant,
            'moderator': self.moderator, 'target': self.target,
            'channel': self.channel, 'guild': self.guild,
            'reason': self.reason, 'edits': self.edits
        }


class IncidentCore(object):
    def __init__(self, db: Database):
        self.db = db
        self.coll = self.db[self.db.db_nam].Incidents

    async def get(self, guild: int, token: str, variant: str):
        incident = None
        lookup = {'id': token, 'variant': variant, 'guild.id': guild}
        incident_doc = await self.coll.find_one(lookup)
        if incident_doc is not None:
            incident = Incident(incident_doc)
        return incident

    @staticmethod
    def generate(variant: str):
        token = secrets.token_hex(4)
        return Incident({'id': token, 'variant': variant})

    async def save(self, incident: Incident):
        await self.coll.insert_one(incident.to_dict())
