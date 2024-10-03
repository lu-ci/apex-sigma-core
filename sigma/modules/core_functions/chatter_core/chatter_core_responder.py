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
import json
import re
from typing import Optional

import aiohttp
import arrow

from sigma.modules.core_functions.chatter_core.chatter_core_init import chatter_core, train
from sigma.modules.utilities.mathematics.nodes.encryption import get_encryptor

OLLAMA_URI = 'http://localhost:11434'
OLLAMA_MODEL = 'sigma:latest'
MESSAGE_STORE = {}


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


def clean_llm_response(msg: str) -> str:
    new = []
    pieces = msg.split(' ')
    for ix, piece in enumerate(pieces):
        if not (ix == 0 and piece.endswith(':')):
            new.append(piece)
    return ' '.join(new)


def get_key(ev, pld) -> str:
    stored_key = pld.settings.get('cb_ai_key')
    if stored_key:
        encrpted_key = stored_key.encode('utf-8')
        cipher = get_encryptor(ev.bot.cfg)
        decrypted_key = cipher.decrypt(encrpted_key)
        parsed_key = decrypted_key.decode('utf-8')
    else:
        parsed_key = None
    return parsed_key


def get_endpoint(pld) -> Optional[str]:
    return pld.settings.get('cb_ai_endpoint')


def get_model(pld) -> Optional[str]:
    return pld.settings.get('cb_ai_model')


def get_directive(pld) -> Optional[str]:
    directive = pld.settings.get('cb_ai_directive')
    if not directive:
        directive = "You are Sigma, an AI chat bot. Respond to users in short sentences and add some emoji too."
    return directive


async def get_custom_response(ev, pld, message) -> str:
    key = get_key(ev, pld)
    endpoint = get_endpoint(pld)
    model = get_model(pld)
    if not key and not endpoint and not model:
        cbconf = ev.bot.modules.commands.get('chatterbot').cfg
        key = cbconf.get('ai_key')
        endpoint = cbconf.get('ai_endpoint')
        model = cbconf.get('ai_model')
    directive = get_directive(pld)
    headers = {'Content-Type': 'application/json'}
    if key:
        headers.update({'Authorization': f'Bearer {key}'})
    if 'openrouter.ai' in endpoint:
        headers.update({
            'HTTP-Referer': 'https://luciascipher.com/sigma',
            'X-Title': 'Apex Sigma'
        })
    context = f'The user\'s Discord name who sent the following message is {pld.msg.author.nick}.'
    context += f'\nThe Discord channel you are talking in is #{pld.msg.channel.name}.'
    context += f'\nThe Discord server name is {pld.msg.guild.name}.'
    context += f'\nThe current date and time is {arrow.utcnow().format("YYYY-MM-DD HH:mm:SS")} UTC.'
    if pld.msg.reference:
        referenced = pld.msg.reference.resolved
        if referenced.author.id == ev.bot.user.id:
            context += f'\nTheir message is a reply to your message saying: {referenced.content}'
        else:
            author = referenced.author.nick
            context += f'\nTheir message is a reply to a message from {author} saying: {referenced.content}'
    messages = MESSAGE_STORE.get(pld.msg.guild.id, [])[-20:]
    if not messages:
        messages = [
            {
                'role': 'system',
                'content': directive,
            }
        ]
    messages += [
        {
            'role': 'system',
            'content': context
        },
        {
            'role': 'user',
            'content': message
        }
    ]
    MESSAGE_STORE.update({pld.msg.guild.id: messages})
    payload = {
        'stream': False,
        'model': model,
        'messages': messages
    }
    # noinspection PyBroadException
    try:
        failed = False
        error_message = None
        async with aiohttp.ClientSession(read_timeout=60, conn_timeout=60) as session:
            async with session.post(endpoint, data=json.dumps(payload), headers=headers) as resp:
                body = await resp.text()
                data = json.loads(body)
        if data.get('error'):
            failed = True
            error_message = data.get('error', {}).get('message')
    except Exception as e:
        failed = True
        error_message = str(e)
    if failed:
        response = f'Something went wrong: {error_message}'
    else:
        if "choices" in data:
            data = data['choices'][0]
        response = data.get('message').get('content')
    return response


async def chatter_core_responder(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.content:
        start_one = check_start(pld.msg, ev.bot.user.id)
        start_two = pld.msg.reference.resolved.author.id == ev.bot.user.id if pld.msg.reference else False
        if start_one or start_two:
            clean_msg = pld.msg.clean_content.replace('@', '')
            if start_one:
                clean_msg = clean_msg.partition(' ')[2]
            if clean_msg:
                setting = pld.settings.get('chatterbot')
                ai_mode = pld.settings.get('cb_ai_mode')
                if ai_mode != 'custom':
                    active = setting in [True, None] or pld.msg.author.id in ev.bot.cfg.dsc.owners
                    is_owner = pld.msg.author.id in ev.bot.cfg.dsc.owners
                    if clean_msg.lower() == 'reset prefix':
                        if pld.msg.channel.permissions_for(pld.msg.author).manage_guild or is_owner:
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
                            sleep_time = min(len(response_text.split(' ')) * 0.58, 10.0)
                            await asyncio.sleep(sleep_time)
                            await pld.msg.reply(response_text)
                else:
                    async with pld.msg.channel.typing():
                        try:
                            response_text = await get_custom_response(ev, pld, clean_msg)
                        except Exception as err:
                            response_text = f'Broad error: {err}'
                        await pld.msg.reply(response_text)
