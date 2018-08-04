# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

from sigma.core.mechanics.caching import Cacher

perm_cache = Cacher()


def generate_default_data(message):
    return {
        'server_id': message.guild.id,
        'DisabledCommands': [], 'DisabledModules': [],
        'CommandExceptions': {}, 'ModuleExceptions': {},
    }


def generate_cmd_data(cmd_name):
    return {cmd_name: {'Users': [], 'Channels': [], 'Roles': []}}


async def get_all_perms(db, message):
    perms = perm_cache.get_cache(message.guild.id)
    if not perms:
        perms = await db[db.db_nam].Permissions.find_one({'server_id': message.guild.id})
        if not perms:
            perms = generate_default_data(message)
            await db[db.db_nam].Permissions.insert_one(perms)
        perm_cache.set_cache(message.guild.id, perms)
    return perms
