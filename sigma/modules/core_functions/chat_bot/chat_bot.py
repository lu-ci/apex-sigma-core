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
import json

import aiohttp
import discord

from sigma.core.mechanics.event import SigmaEvent


cb_api = 'https://api.lucia.moe/rest/sigma/chatterbot'


def clean_mentions(members, text):
    text = str(text)
    args = text.split(' ')
    out = []
    for arg in args:
        if arg.startswith('<@') and arg.endswith('>'):
            try:
                uid = arg[2:-1]
                user = discord.utils.find(lambda x: x.id == int(uid), members)
                if user:
                    addition = user.name
                else:
                    addition = 'Someone'
            except ValueError:
                addition = 'Someone'
        else:
            addition = arg
        out.append(addition)
    return ' '.join(out)


async def chat_bot(ev: SigmaEvent, message: discord.Message):
    try:
        args = message.content.split(' ')
        if len(args) > 1:
            if message.guild:
                active = await ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
                if active:
                    mention = f'<@{ev.bot.user.id}>'
                    mention_alt = f'<@!{ev.bot.user.id}>'
                    if message.content.startswith(mention) or message.content.startswith(mention_alt):
                        interaction = ' '.join(args[1:])
                        if interaction:
                            async with aiohttp.ClientSession() as session:
                                api_data = await session.post(cb_api, json={'interaction': interaction})
                                api_bytes = await api_data.read()
                            cb_data = json.loads(api_bytes)
                            cb_resp = cb_data.get('response')
                            if not cb_resp:
                                cb_resp = 'Sorry bud, I\'m not feeling too well, let\'s talk later...'
                            cb_resp = clean_mentions(ev.bot.get_all_members(), cb_resp)
                            response = f'<:lcSigma:281523687725989898> | {message.author.mention} {cb_resp}'
                            await message.channel.send(response)
    except IndexError:
        pass
