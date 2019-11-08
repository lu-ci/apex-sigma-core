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

import re

import arrow
import discord

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig
from sigma.core.utilities.generic_responses import error, not_found

emote_cache_handler = MemoryCacher(CacheConfig({}))


async def get_emote_cache(cmd):
    """
    Gets all emotes the client is exposed to.
    :param cmd: The main command instance reference.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :return:
    :rtype: list
    """
    fill = False
    emote_cache = await emote_cache_handler.get_cache('emote_cache')
    if not emote_cache:
        fill = True
    elif arrow.utcnow().timestamp > emote_cache.get('stamp') + 300:
        fill = True
    if fill:
        all_emotes = list(cmd.bot.emojis)
        await emote_cache_handler.set_cache('emote_cache', {'stamp': arrow.utcnow().timestamp, 'emotes': all_emotes})
    else:
        all_emotes = emote_cache.get('emotes')
    return all_emotes


def get_emote(emoji):
    """
    Gets a specific emote by lookup.
    :param emoji: The emote to get.
    :type emoji: str or discord.Emoji
    :return:
    :rtype: (str, int)
    """
    lookup, eid = emoji, None
    if ':' in emoji:
        # matches custom emote
        server_match = re.search(r'<a?:(\w+):(\d+)>', emoji)
        # matches global emote
        custom_match = re.search(r':(\w+):', emoji)
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


async def emote(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        nsfw = True
        lookup, eid = pld.args[0].lower(), None
        if ':' in lookup:
            lookup, eid = get_emote(lookup)
        if pld.args[-1].lower() == '--global':
            all_emotes = await get_emote_cache(cmd)
        else:
            all_emotes = pld.msg.guild.emojis
            nsfw = False
        if eid:
            emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.id == eid, all_emotes)
            if not emote_choice:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == eid, all_emotes)
        else:
            sid = pld.msg.guild.id
            emote_priority = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == sid, all_emotes)
            if emote_priority:
                emote_choice = emote_priority
            else:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup, all_emotes)
        if not nsfw or pld.msg.channel.is_nsfw():
            if emote_choice:
                response = discord.Embed().set_image(url=emote_choice.url)
            else:
                response = not_found('Emote not found.')
        else:
            response = error('Emotes from other servers can be NSFW.')
            response.description = 'Mark this channel as NSFW or move to one that is.'
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
