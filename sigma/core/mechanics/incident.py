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
        self.order = self.data.get('order')
        self.variant = self.data.get('variant')
        self.moderator = IncidentUser(self.data.get('moderator'))
        self.target = IncidentUser(self.data.get('target'))
        self.channel = IncidentLocation(self.data.get('channel'))
        self.guild = IncidentLocation(self.data.get('guild'))
        self.reason = self.data.get('reason')
        self.edits = self.data.get('edits', [])
        self.timestamp = self.data.get('timestamp')

    @property
    def last_edited(self, formatted=False):
        last_edit_stamp = None
        if self.edits:
            sorted_edits = sorted(self.edits, key=lambda ed: ed.get('timestamp', 0), reverse=True)
            last_edit_stamp = sorted_edits[0].get('timestamp')
        if formatted:
            if last_edit_stamp:
                last_edit_stamp = 'Never'
            else:
                last_edit_stamp = arrow.get(last_edit_stamp).format("DD. MMM. YYYY HH:mm:ss (ZZ)")
        return last_edit_stamp

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
        del previous['edits']
        self.reason = reason
        by = IncidentUser(user)
        when = arrow.utcnow().float_timestamp
        self.edits.append({'moderator': by.to_dict(), 'timestamp': when, 'previous': previous})

    def to_dict(self):
        return {
            'id': self.id, 'order': self.order, 'variant': self.variant,
            'moderator': self.moderator, 'target': self.target,
            'channel': self.channel, 'guild': self.guild,
            'reason': self.reason, 'edits': self.edits,
            'timestamp': self.timestamp
        }

    def to_text(self):
        if self.data.get('moderator'):
            moderator = f'{self.moderator.name}#{self.moderator.discriminator} [{self.moderator.id}]'
        else:
            moderator = "Unknown Mod"
        if self.data.get('target'):
            target = f'{self.target.name}#{self.target.discriminator} [{self.target.id}]'
        else:
            target = "Unknown User"
        if self.data.get('channel'):
            location = f'in #{self.channel.name} [{self.channel.id}] on {self.guild.name} [{self.guild.id}]'
        else:
            location = f'on {self.guild.name} [{self.guild.id}]'
        if self.data.get('timestamp'):
            date_time = arrow.get(self.timestamp).format("DD. MMM. YYYY HH:mm:ss (ZZ)")
        else:
            date_time = "Unknown Date and Time"
        output = f'{self.id}: {self.variant.title() if self.variant else "Unknown"} incident by '
        output += f'{moderator} affecting {target} {location} on {date_time}'
        return output


class IncidentCore(object):
    def __init__(self, db: Database):
        self.db = db
        self.coll = self.db[self.db.db_nam].Incidents

    async def get(self, guild: int, identifier: str, value: str or int):
        incident = None
        lookup = {identifier: value, 'guild.id': guild}
        incident_doc = await self.coll.find_one(lookup)
        if incident_doc is not None:
            incident = Incident(incident_doc)
        return incident

    async def get_by_token(self, guild: int, token: str):
        return await self.get(guild, 'id', token)

    async def get_by_order(self, guild: int, order: int):
        await self.get(guild, 'order', order)

    async def get_all(self, guild: int, variant: str = None):
        incidents = []
        lookup = {'guild.id': guild} if variant is None else {'guild.id': guild, 'variant': variant}
        incident_docs = await self.coll.find(lookup).to_list(None)
        for incident_doc in incident_docs:
            incident = Incident(incident_doc)
            incidents.append(incident)
        return incidents

    async def count_incidents(self, guild: int):
        return await self.coll.count_documents({'guild.id': guild})

    @staticmethod
    async def generate(variant: str):
        return Incident({
            'id': secrets.token_hex(4),
            'variant': variant,
            'timestamp': arrow.utcnow().float_timestamp
        })

    async def save(self, incident: Incident):
        lookup = {'id': incident.id, 'guild.id': incident.guild.id}
        lookup_doc = await self.coll.find_one(lookup)
        if lookup:
            await self.coll.update_one({lookup_doc}, {'$set': incident.to_dict()})
        else:
            incident.order = (await self.count_incidents(incident.guild.id)) + 1
            await self.coll.insert_one(incident.to_dict())
