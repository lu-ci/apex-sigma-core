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

import re
import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand

emote_cache = {'stamp': 0, 'emotes': []}


def get_emote(emoji: str or discord.Emoji):
    lookup, eid = emoji, None
    if ':' in emoji:
        server_match = re.match(r'^<a?:(\w+):(\d+)>$', emoji)
        custom_match = re.match(r'^:(\w+):$', emoji)
        if server_match:
            lookup, eid = server_match.group(1), server_match.group(2)
        elif custom_match:
            lookup, eid = custom_match.group(1), None
        else:
            lookup, eid = emoji.split(':')
        try:
            eid = int(eid)
        except (ValueError, TypeError):
            eid = None
    return lookup, eid


async def emote(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup, eid = args[0].lower(), None
        if ':' in lookup:
            lookup, eid = get_emote(lookup)
        if arrow.utcnow().timestamp > emote_cache.get('stamp') + 300:
            all_emotes = cmd.bot.emojis
            emote_cache.update({'stamp': arrow.utcnow().timestamp, 'emotes': all_emotes})
        else:
            all_emotes = emote_cache.get('emotes')
        if eid:
            emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.id == eid, all_emotes)
            if not emote_choice:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == eid, all_emotes)
        else:
            sid = message.guild.id
            emote_priority = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == sid, all_emotes)
            if emote_priority:
                emote_choice = emote_priority
            else:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup, all_emotes)
        if emote_choice:
            response = discord.Embed().set_image(url=emote_choice.url)
        else:
            response = discord.Embed(color=0x696969, title='🔍 Emote not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
