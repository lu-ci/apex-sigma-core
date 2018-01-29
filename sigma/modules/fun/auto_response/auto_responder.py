# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import string

from sigma.core.utilities.data_processing import command_message_parser


def clean_word(text):
    output = ''
    for char in text:
        if char.lower() not in string.punctuation:
            output += char.lower()
    return output


async def auto_responder(ev, message):
    if message.guild:
        if message.content:
            pfx = await ev.bot.get_prefix(message)
            if not message.content.startswith(pfx):
                triggers = await ev.db.get_guild_settings(message.guild.id, 'ResponderTriggers')
                if triggers is None:
                    triggers = {}
                arguments = message.content.split(' ')
                for arg in arguments:
                    arg = clean_word(arg)
                    if arg in triggers:
                        response = triggers[arg]
                        response = command_message_parser(message, response)
                        await message.channel.send(response)
                        break
