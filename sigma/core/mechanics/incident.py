# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
    def __init__(self, entity: dict or discord.Member or discord.User = None):
        self.entity = entity
        if isinstance(entity, dict):
            self.from_dict(entity)
        elif isinstance(entity, discord.Member) or isinstance(entity, discord.User):
            self.from_user(entity)
        else:
            self.id = None
            self.name = None
            self.discriminator = None

    def from_user(self, user: discord.Member or discord.User):
        self.id = user.id
        self.name = user.name
        self.discriminator = user.discriminator

    def from_dict(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name')
        self.discriminator = data.get('discriminator')

    def to_text(self, in_embed=True):
        if in_embed:
            output = f'<@{self.id}>\n{self.name}#{self.discriminator}'
        else:
            output = f'{self.name}#{self.discriminator} [{self.id}]'
        return output

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'discriminator': self.discriminator}


class IncidentLocation(object):
    def __init__(self, entity: dict or discord.TextChannel or discord.Guild = None):
        self.entity = entity
        self.variant = None
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
        if isinstance(obj, discord.TextChannel):
            self.variant = 'channel'
        else:
            self.variant = 'guild'

    def from_dict(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name')

    def to_text(self, in_embed=True):
        name_piece = f'#{self.name}' if self.variant == 'channel' else self.name
        mention_piece = f'<#{self.id}>' if self.variant == 'channel' else None
        if in_embed:
            output = f'{mention_piece if mention_piece else ""}'
            output += f'{name_piece}'
        else:
            output = f'{name_piece} [{self.id}]'
        return output

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
            if not last_edit_stamp:
                last_edit_stamp = 'Never'
            else:
                last_edit_stamp = arrow.get(last_edit_stamp).format("DD. MMM. YYYY HH:mm:ss (ZZ)")
        return last_edit_stamp

    def set_moderator(self, user: discord.Member or discord.User):
        self.moderator = IncidentUser(user)

    def set_target(self, user: discord.Member or discord.User):
        self.target = IncidentUser(user)

    def set_location(self, location: discord.TextChannel or discord.Guild):
        if isinstance(location, discord.TextChannel):
            self.channel = IncidentLocation(location)
            self.guild = IncidentLocation(location.guild)
        else:
            self.guild = IncidentLocation(location)

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
            'moderator': self.moderator.to_dict(), 'target': self.target.to_dict(),
            'channel': self.channel.to_dict(), 'guild': self.guild.to_dict(),
            'reason': self.reason, 'edits': self.edits,
            'timestamp': self.timestamp
        }

    def to_text(self):
        if all(self.data.get('moderator').values()):
            moderator = f'{self.moderator.to_text(False)}'
        else:
            moderator = "Unknown Mod"
        if all(self.data.get('target').values()):
            target = f'{self.target.to_text(False)}'
        else:
            target = "Unknown User"
        if all(self.data.get('channel').values()):
            location = f'in {self.channel.to_text(False)} on {self.guild.to_text(False)}'
        else:
            location = f'on {self.guild.to_text(False)}'
        if self.data.get('timestamp'):
            date_time = arrow.get(self.timestamp).format("DD. MMM. YYYY HH:mm:ss (ZZ)")
        else:
            date_time = "Unknown Date and Time"
        output = f'{self.id}: {self.variant.title() if self.variant else "Unknown"} incident by '
        output += f'{moderator} affecting {target} {location} on {date_time}'
        return output

    def to_embed(self, icon: str, color: int):
        incident_title = f'{self.variant.title()} incident recorded.'
        response = discord.Embed(color=color, timestamp=arrow.utcnow().datetime, title=incident_title)
        response.add_field(name=f'{icon} Target', value=self.target.to_text())
        response.add_field(name='🛡 Moderator', value=self.moderator.to_text())
        if self.reason:
            response.add_field(name='📄 Reason', value=f'```\n{self.reason}\n```', inline=False)
        response.set_footer(text=f'Incident ID: {self.id} | Incident Number: {self.order}')
        return response


class IncidentCore(object):
    def __init__(self, db: Database):
        self.db = db
        self.coll = self.db[self.db.db_nam].Incidents

    async def get(self, guild_id: int, identifier: str, value: str or int):
        incident = None
        lookup = {identifier: value, 'guild.id': guild_id}
        incident_doc = await self.coll.find_one(lookup)
        if incident_doc is not None:
            incident = Incident(incident_doc)
        return incident

    async def get_by_token(self, guild_id: int, token: str):
        return await self.get(guild_id, 'id', token)

    async def get_by_order(self, guild_id: int, order: int):
        return await self.get(guild_id, 'order', order)

    async def get_all(self, guild_id: int, identifier: int or str = None, identifier_id: int or str = None):
        incidents = []
        lookup = {'guild.id': guild_id} if identifier is None else {'guild.id': guild_id, identifier: identifier_id}
        incident_docs = await self.coll.find(lookup).to_list(None)
        for incident_doc in incident_docs:
            incident = Incident(incident_doc)
            incidents.append(incident)
        return incidents

    async def get_all_by_variant(self, guild_id: int, variant: str):
        return await self.get_all(guild_id, 'variant', variant)

    async def get_all_by_mod(self, guild_id: int, mod_id: int):
        return await self.get_all(guild_id, 'moderator.id', mod_id)

    async def get_all_by_target(self, guild_id: int, target_id: int):
        return await self.get_all(guild_id, 'target.id', target_id)

    async def count_incidents(self, guild_id: int):
        return await self.coll.count_documents({'guild.id': guild_id})

    @staticmethod
    def generate(variant: str):
        return Incident({
            'id': secrets.token_hex(4),
            'variant': variant,
            'timestamp': arrow.utcnow().float_timestamp
        })

    async def save(self, incident: Incident):
        lookup = {'id': incident.id, 'guild.id': incident.guild.id}
        lookup_doc = await self.coll.find_one(lookup)
        if lookup_doc:
            await self.coll.update_one(lookup_doc, {'$set': incident.to_dict()})
        else:
            incident.order = (await self.count_incidents(incident.guild.id)) + 1
            await self.coll.insert_one(incident.to_dict())

    async def report(self, guild: discord.Guild, incident_embed: discord.Embed):
        incident_channel_id = await self.db.get_guild_settings(guild.id, 'log_incidents_channel')
        incident_channel = guild.get_channel(incident_channel_id)
        if incident_channel:
            try:
                await incident_channel.send(embed=incident_embed)
            except (discord.Forbidden, discord.NotFound):
                pass
