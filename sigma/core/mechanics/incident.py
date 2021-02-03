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

import secrets

import arrow
import discord

incident_core_cache = None


def get_incident_core(db):
    """
    Grabs a cached incident core
    so it isn't initialized every time it's needed.
    :param db: The core database instance.
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: sigma.core.mechanics.incident.IncidentCore
    """
    global incident_core_cache
    if incident_core_cache is None:
        incident_core_cache = IncidentCore(db)
    return incident_core_cache


class IncidentUser(object):
    """
    An abstraction class for handling incident user data.
    """

    __slots__ = ("entity", "id", "name", "discriminator")

    def __init__(self, entity=None):
        """
        :param entity: User data storage.
        :type entity: dict or discord.Member or discord.User
        """
        self.entity = entity
        if isinstance(entity, dict):
            self.from_dict(entity)
        elif isinstance(entity, discord.Member) or isinstance(entity, discord.User):
            self.from_user(entity)
        else:
            self.id = None
            self.name = None
            self.discriminator = None

    def from_user(self, user):
        """
        Parses data from a discord user object.
        :param user: The user to parse the data from.
        :type user: discord.Member or discord.User
        """
        self.id = user.id
        self.name = user.name
        self.discriminator = user.discriminator

    def from_dict(self, data):
        """
        Parses data from a dict document.
        :param data: The dict to grab the data from.
        :type data: dict
        """
        self.id = data.get('id')
        self.name = data.get('name')
        self.discriminator = data.get('discriminator')

    def to_text(self, in_embed=True):
        """
        Mames a text block of the user's information.
        :param in_embed: Is this in an embed message response or log line.
        :type in_embed: bool
        :return:
        :rtype: str
        """
        if in_embed:
            output = f'<@{self.id}>\n{self.name}#{self.discriminator}'
        else:
            output = f'{self.name}#{self.discriminator} [{self.id}]'
        return output

    def to_dict(self):
        """
        Converts all data to a dict document.
        :return:
        :rtype: dict
        """
        return {'id': self.id, 'name': self.name, 'discriminator': self.discriminator}


class IncidentLocation(object):
    """
    An abstraction class for handling incident location data.
    """

    def __init__(self, entity=None):
        """
        :param entity: The entity to get the location data from.
        :type entity: dict or discord.TextChannel or discord.Guild
        """
        self.entity = entity
        self.variant = None
        if isinstance(entity, dict):
            self.from_dict(entity)
        elif isinstance(entity, discord.TextChannel) or isinstance(entity, discord.Guild):
            self.from_obj(entity)
        else:
            self.id = None
            self.name = None

    def from_obj(self, obj):
        """
        Parses the location data from an object.
        :param obj: The object from which to get the data from.
        :type obj: discord.TextChannel or discord.Guild
        """
        self.id = obj.id
        self.name = obj.name
        if isinstance(obj, discord.TextChannel):
            self.variant = 'channel'
        else:
            self.variant = 'guild'

    def from_dict(self, data):
        """
        Parses the location data from a dict document.
        :param data: Dict data to parse for the class.
        :type data: dict
        """
        self.id = data.get('id')
        self.name = data.get('name')

    def to_text(self, in_embed=True):
        """
        Mames a text block of the location information.
        :param in_embed: Is this in an embed message response or log line.
        :type in_embed: bool
        :return:
        :rtype: str
        """
        name_piece = f'#{self.name}' if self.variant == 'channel' else self.name
        mention_piece = f'<#{self.id}>' if self.variant == 'channel' else None
        if in_embed:
            output = f'{mention_piece if mention_piece else ""}'
            output += f'{name_piece}'
        else:
            output = f'{name_piece} [{self.id}]'
        return output

    def to_dict(self):
        """
        Converts all data to a dict document.
        :return:
        :rtype: dict
        """
        return {'id': self.id, 'name': self.name}


class Incident(object):
    """
    An incident data wrapper class.
    Handlest quick formatting and descriptions of incidents.
    """

    def __init__(self, data=None):
        """
        :param data: The incident data to parse into the class.
        :type data: dict
        """
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
        """
        Gets the last edited timestamp.
        :param formatted: Should the timestamp be formatted into a human readable format.
        :type formatted: bool
        :return:
        :rtype: int or float or str
        """
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

    def set_moderator(self, user):
        """
        Sets the moderator in charge of the generated incident.
        :param user: The moderator's user object.
        :type user: discord.Member or discord.User
        """
        self.moderator = IncidentUser(user)

    def set_target(self, user):
        """
        Sets the affected target of the incident event.
        :param user: The target's user object.
        :type user: discord.Member or discord.User
        """
        self.target = IncidentUser(user)

    def set_location(self, location):
        """
        Sets the location in which the event was triggered.
        :param location: The location's object.
        :type location: discord.TextChannel or discord.Guild
        """
        if isinstance(location, discord.TextChannel):
            self.channel = IncidentLocation(location)
            self.guild = IncidentLocation(location.guild)
        else:
            self.guild = IncidentLocation(location)

    def set_reason(self, text):
        """
        Sets the reason/description of the incident.
        :param text: The reason text contents.
        :type text: str
        """
        self.reason = text

    def edit(self, user, reason):
        """
        Edits the incident reason/description
        and stores the user who edited it.
        :param user: The user that edited the description.
        :type user: discord.Member or discord.User
        :param reason: The new reason text contents.
        :type reason: str
        """
        previous = self.to_dict()
        del previous['edits']
        self.reason = reason
        by = IncidentUser(user)
        when = arrow.utcnow().float_timestamp
        self.edits.append({'moderator': by.to_dict(), 'timestamp': when, 'previous': previous})

    def to_dict(self):
        """
        Converts the incident data class to a dictionary document.
        :return:
        :rtype: dict
        """
        return {
            'id': self.id, 'order': self.order, 'variant': self.variant,
            'moderator': self.moderator.to_dict(), 'target': self.target.to_dict(),
            'channel': self.channel.to_dict(), 'guild': self.guild.to_dict(),
            'reason': self.reason, 'edits': self.edits,
            'timestamp': self.timestamp
        }

    def to_text(self):
        """
        Describes the incident in a textual form.
        :return:
        :rtype: str
        """
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

    def to_embed(self, icon, color):
        """
        Describes the incident in a discord embed.
        :param icon: The icon to use for the incident.
        :type icon: str
        :param color: The color to use for the incident embed strip.
        :type color: int
        :return:
        :rtype: discord.Embed
        """
        incident_title = f'{self.variant.title()} incident recorded.'
        response = discord.Embed(color=color, timestamp=arrow.utcnow().datetime, title=incident_title)
        response.add_field(name=f'{icon} Target', value=self.target.to_text())
        response.add_field(name='🛡 Moderator', value=self.moderator.to_text())
        if self.reason:
            response.add_field(name='📄 Reason', value=f'```\n{self.reason}\n```', inline=False)
        response.set_footer(text=f'Incident ID: {self.id} | Incident Number: {self.order}')
        return response


class IncidentCore(object):
    """
    The main incident handler core.
    One core can handle all incident processing.
    """

    def __init__(self, db):
        self.db = db
        self.coll = self.db[self.db.db_nam].Incidents

    async def get(self, guild_id, identifier, value):
        """
        Gets a single incident from a guild's document
        storage based on the incident identifier key and value.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param identifier: The lookup identifier key.
        :type identifier: str
        :param value: The value of the lookup identifier.
        :type value: str or int
        :return:
        :rtype: sigma.core.mechanics.incident.Incident
        """
        incident = None
        lookup = {identifier: value, 'guild.id': guild_id}
        incident_doc = await self.coll.find_one(lookup)
        if incident_doc is not None:
            incident = Incident(incident_doc)
        return incident

    async def get_by_token(self, guild_id, token):
        """
        Gets an incident document by the unique incident token.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param token: The unique indicent token.
        :type token: str
        :return:
        :rtype: sigma.core.mechanics.incident.Incident
        """
        return await self.get(guild_id, 'id', token)

    async def get_by_order(self, guild_id, order):
        """
        Gets an incident document by the incrementing order
        that the incident document was generated with.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param order: The sequential index of the generated index.
        :type order: int
        :return:
        :rtype: sigma.core.mechanics.incident.Incident
        """
        return await self.get(guild_id, 'order', order)

    async def get_all(self, guild_id, identifier=None, identifier_id=None):
        """
        Gets all incidents with the given criteria.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param identifier: The identifier lookup key.
        :type identifier: int or str
        :param identifier_id: The identifier lookup value.
        :type identifier_id: int or str
        :return:
        :rtype: list[sigma.core.mechanics.incident.Incident]
        """
        incidents = []
        lookup = {'guild.id': guild_id} if identifier is None else {'guild.id': guild_id, identifier: identifier_id}
        incident_docs = await self.coll.find(lookup).to_list(None)
        for incident_doc in incident_docs:
            incident = Incident(incident_doc)
            incidents.append(incident)
        return incidents

    async def get_all_by_variant(self, guild_id, variant):
        """
        Gets a list of all incidents by incident variant.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param variant: The incident variant identifier.
        :type variant: str
        :return:
        :rtype: list[sigma.core.mechanics.incident.Incident]
        """
        return await self.get_all(guild_id, 'variant', variant)

    async def get_all_by_mod(self, guild_id, mod_id):
        """
        Gets a list of all incidents by the incident's moderator.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param mod_id: The moderator's User ID.
        :type mod_id: int
        :return:
        :rtype: list[sigma.core.mechanics.incident.Incident]
        """
        return await self.get_all(guild_id, 'moderator.id', mod_id)

    async def get_all_by_target(self, guild_id, target_id):
        """
        Gets a list of all incidents by the incident's target user.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :param target_id: The target's User ID.
        :type target_id: int
        :return:
        :rtype: list[sigma.core.mechanics.incident.Incident]
        """
        return await self.get_all(guild_id, 'target.id', target_id)

    async def count_incidents(self, guild_id):
        """
        Counts all incidents for the given guild.
        :param guild_id: The Guild ID.
        :type guild_id: int
        :return:
        :rtype: int
        """
        return await self.coll.count_documents({'guild.id': guild_id})

    @staticmethod
    def generate(variant):
        """
        Generates an incident class with basic data.
        :param variant: The incident's variant/type.
        :type variant: str
        :return:
        :rtype: sigma.core.mechanics.incident.Incident
        """
        return Incident({
            'id': secrets.token_hex(4),
            'variant': variant,
            'timestamp': arrow.utcnow().float_timestamp
        })

    async def save(self, incident):
        """
        Saves the data from an incident class to the database.
        :param incident: The incident to save.
        :type incident: sigma.core.mechanics.incident.Incident
        """
        lookup = {'id': incident.id, 'guild.id': incident.guild.id}
        lookup_doc = await self.coll.find_one(lookup)
        if lookup_doc:
            await self.coll.update_one(lookup_doc, {'$set': incident.to_dict()})
        else:
            incident.order = (await self.count_incidents(incident.guild.id)) + 1
            await self.coll.insert_one(incident.to_dict())

    async def report(self, guild, incident_embed):
        """
        Reports the incident's contents to the guild's incident channel.
        :param guild: The guild that the incident happened in.
        :type guild: discord.Guild
        :param incident_embed: The incident embed to send to the guild's incident channel.
        :type incident_embed: discord.Embed
        """
        incident_channel_id = await self.db.get_guild_settings(guild.id, 'log_incidents_channel')
        incident_channel = guild.get_channel(incident_channel_id)
        if incident_channel:
            try:
                await incident_channel.send(embed=incident_embed)
            except (discord.Forbidden, discord.NotFound):
                pass
