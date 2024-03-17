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
import secrets

from sigma.modules.core_functions.chatter_core.mech.relay import RelayHandler

OLLAMA_URI = 'http://localhost:11434'
OLLAMA_MODEL = 'sigma:latest'
MESSAGE_STORE = {}

AI_CORE = None


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
    global AI_CORE
    if pld.msg.content:
        start_one = check_start(pld.msg, ev.bot.user.id)
        start_two = pld.msg.reference.resolved.author.id == ev.bot.user.id if pld.msg.reference else False
        if start_one or start_two:
            clean_msg = pld.msg.clean_content.replace('@', '')
            if start_one:
                clean_msg = clean_msg.partition(' ')[2]
            if clean_msg:
                setting = pld.settings.get('chatterbot')
                active = setting in [True, None] or pld.msg.author.id in ev.bot.cfg.dsc.owners
                if clean_msg.lower() == 'reset prefix':
                    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
                        await ev.db.set_guild_settings(pld.msg.guild.id, 'prefix', None)
                        response = f'The prefix for this server has been reset to `{ev.bot.cfg.pref.prefix}`.'
                    else:
                        response = 'You don\'t have the Manage Server permission, so no, I won\'t do that.'
                    await pld.msg.channel.send(response)
                elif active:
                    if AI_CORE is None:
                        AI_CORE = RelayHandler(ev.db)
                        await AI_CORE.clean()
                    async with pld.msg.channel.typing():
                        token = secrets.token_hex(4)
                        await AI_CORE.store(token, pld.msg.channel.id, pld.msg.author.display_name, clean_msg)
                        response_text = await AI_CORE.wait_for_reply(token)
                        if response_text:
                            await pld.msg.reply(response_text)
                        else:
                            await pld.msg.reply('Sorry, handling your message timed out.')

