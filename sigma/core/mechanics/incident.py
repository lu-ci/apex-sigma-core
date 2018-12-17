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

import discord


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


class Incident(object):
    def __init__(self, data: dict):
        self.data = data if data is not None else {}
        self.id = data.get('id')
        self.incident_type = data.get('type')
        self.moderator = data.get('moderator')
        self.target = data.get('target')

    def set_mod(self, user: discord.Member):
        self.moderator = IncidentUser(user)

    def to_dict(self):
        return {'id': self.id, 'type': self.incident_type, 'moderator': self.moderator, 'target': self.target}
