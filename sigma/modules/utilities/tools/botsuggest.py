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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import ok, error


def make_sugg_data(msg: discord.Message, args: list, token: str):
    return {
        'suggestion': {
            'id': token,
            'text': ' '.join(args)
        },
        'user': {
            'id': msg.author.id,
            'name': msg.author.name,
            'color': msg.author.color.value,
            'avatar': user_avatar(msg.author)
        },
        'guild': {
            'id': msg.guild.id,
            'name': msg.guild.name,
            'icon': msg.guild.icon_url
        },
        'timestamp': msg.created_at.timestamp(),
        'reported': False
    }


async def botsuggest(cmd: SigmaCommand, pld: CommandPayload):
    coll = cmd.db[cmd.db.db_nam].Suggestions
    sugg_chn_id = cmd.cfg.get('channel')
    if sugg_chn_id:
        if pld.args:
            sugg_token = secrets.token_hex(4)
            await coll.insert_one(make_sugg_data(pld.msg, pld.args, sugg_token))
            response = ok(f'Suggestion {sugg_token} submitted.')
        else:
            response = error('Nothing inputted.')
    else:
        response = error('Missing suggestion channel configuration.')
    await pld.msg.channel.send(embed=response)
