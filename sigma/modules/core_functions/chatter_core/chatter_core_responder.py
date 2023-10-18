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

import asyncio
import re

import discord
from sigma.modules.core_functions.chatter_core.chatter_core_init import chatter_core, train


def set_session_info(pld):
    """
    Sets basic session information depending on the user.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    chatter_core.setPredicate('hostname', pld.msg.guild.name, pld.msg.author.id)
    chatter_core.setPredicate('name', pld.msg.author.name, pld.msg.author.id)
    chatter_core.setPredicate('nickname', pld.msg.author.display_name, pld.msg.author.id)
    chatter_core.setBotPredicate('nickname', pld.msg.guild.me.display_name)
    chatter_core.setBotPredicate('name', pld.msg.guild.me.name)


def clean_response(text):
    """
    :type text: str
    :rtype: str
    """
    new = text
    while '  ' in new:
        new = new.replace('  ', ' ')
    new.replace(' , ', ', ')

    marks = ['.', '!', '?', '...']
    for mark in marks:
        bad_mark = f' {mark}'
        if bad_mark in new:
            new = new.replace(bad_mark, mark)
    return new


def check_start(msg, uid):
    """
    :type msg: discord.Message
    :type uid: int
    :rtype: bool
    """
    return bool(re.match(fr'<@!?{uid}>', msg.content))


async def chatter_core_responder(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.content:
        start_one = check_start(pld.msg, ev.bot.user.id)
        start_two = False
        if pld.msg.reference and isinstance(pld.msg.reference.resolved, discord.Message):
            if pld.msg.guild.me.id == pld.msg.reference.resolved.author.id:
                if check_start(pld.msg.reference.resolved, pld.msg.author.id):
                    start_two = True
        if start_one or start_two:
            clean_msg = pld.msg.clean_content.replace('@', '')
            if start_one:
                clean_msg = clean_msg.partition(' ')[2]
            if clean_msg:
                active = pld.settings.get('chatterbot') or pld.msg.author.id in ev.bot.cfg.owners
                if clean_msg.lower() == 'reset prefix':
                    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
                        await ev.db.set_guild_settings(pld.msg.guild.id, 'prefix', None)
                        response = f'The prefix for this server has been reset to `{ev.bot.cfg.pref.prefix}`.'
                    else:
                        response = 'You don\'t have the Manage Server permission, so no, I won\'t do that.'
                    await pld.msg.channel.send(response)
                elif active:
                    async with pld.msg.channel.typing():
                        if not chatter_core.numCategories():
                            train(ev, chatter_core)
                        set_session_info(pld)
                        response_text = clean_response(chatter_core.respond(clean_msg, pld.msg.author.id))
                        sleep_time = min(len(response_text.split(' ')) * 0.733, 10.0)
                        await asyncio.sleep(sleep_time)
                        await pld.msg.channel.send(f'{pld.msg.author.mention} {response_text}')
