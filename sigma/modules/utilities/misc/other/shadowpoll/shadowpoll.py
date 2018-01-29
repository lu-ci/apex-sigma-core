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
import secrets

import arrow
import discord


def generate_data(message, poll_args):
    uid = message.author.id
    if message.channel:
        cid = message.channel.id
    else:
        cid = None
    if message.guild:
        sid = message.guild.id
    else:
        sid = None
    poll_file_data = {
        'id': secrets.token_hex(3),
        'created': arrow.utcnow().float_timestamp,
        'origin': {
            'author': uid,
            'channel': cid,
            'server': sid
        },
        'poll': {
            'question': poll_args[0],
            'answers': poll_args[1:]
        },
        'votes': {},
        'permissions': {
            'channels': [],
            'users': [],
            'roles': []
        },
        'settings': {
            'visible': False,
            'expires': None,
            'active': True
        }
    }
    return poll_file_data


async def shadowpoll(cmd, message, args):
    if args:
        poll_args = ' '.join(args).split('; ')
        if len(poll_args) >= 3:
            poll_data = generate_data(message, poll_args)
            await cmd.db[cmd.db.db_cfg.database].ShadowPolls.insert_one(poll_data)
            response = discord.Embed(color=0x66CC66, title=f'✅ Shadowpoll `{poll_data["id"]}` has been created.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Too few arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No input given.')
    await message.channel.send(embed=response)
