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


def generate_default_data(message):
    """

    :param message:
    :type message: discord.Message
    :return:
    :rtype: dict
    """
    return {
        'server_id': message.guild.id,
        'disabled_commands': [], 'disabled_modules': [],
        'command_exceptions': {}, 'module_exceptions': {},
    }


def generate_cmd_data(cmd_name):
    """

    :param cmd_name:
    :type cmd_name: str
    :return:
    :rtype: dict
    """
    return {cmd_name: {'users': [], 'channels': [], 'roles': []}}


async def get_all_perms(db, message):
    """

    :param db:
    :type db: sigma.core.mechanics.database.Database
    :param message:
    :type message: discord.Message
    :return:
    :rtype: dict
    """
    perms = await db[db.db_nam].Permissions.find_one({'server_id': message.guild.id})
    if not perms:
        perms = generate_default_data(message)
        await db[db.db_nam].Permissions.insert_one(perms)
    return perms
