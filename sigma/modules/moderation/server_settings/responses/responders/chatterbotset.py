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

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.core_functions.chatter_core.chatter_core_responder import MESSAGE_STORE
from sigma.modules.utilities.mathematics.nodes.encryption import get_encryptor


async def set_mode(cmd, pld, args: list[str]) -> discord.Embed:
    allowed_values = [
        'aiml',
        'custom',
        None
    ]
    if not args:
        val = None
    else:
        val = args[0].lower()
        if val == 'none':
            val = None
    if val in allowed_values:
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_mode', val)
        response = GenericResponse(f'The AI mode has been set to `{val}`.').ok()
        if not val:
            response.description = 'Note that setting the value to none is the same as setting it to AIML.'
    else:
        response = GenericResponse('Unrecognized mode.').error()
        avals = [str(aval).lower() for aval in allowed_values]
        response.description = f'You can select one of these: {", ".join(avals)}.'
    return response


async def set_key(cmd, pld, args: list[str]) -> discord.Embed:
    # noinspection PyBroadException
    try:
        await pld.msg.delete()
        deleted = True
    except Exception:
        deleted = False
    key = ' '.join(args) if args else None
    if key:
        cipher = get_encryptor(cmd.bot.cfg)
        key_encoded = key.encode('utf-8')
        key_encrypted = cipher.encrypt(key_encoded)
        key = key_encrypted.decode('utf-8')
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_key', key)
    if key:
        response = GenericResponse('The key has been updated.').ok()
    else:
        response = GenericResponse('The key has been removed.').ok()
    if deleted:
        response.description = 'The message containing your key has been removed, just in case.'
    else:
        response.description = 'We tried to remove your message containing key but failed, we suggest deleting it.'
    return response


async def set_endpoint(cmd, pld, args: list[str]) -> discord.Embed:
    endpoint = ' '.join(args) if args else None
    if endpoint:
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_endpoint', endpoint)
        response = GenericResponse('The endpoint has been updated.').ok()
    else:
        response = GenericResponse('The endpoint has not been provided.').error()
    return response


async def set_model(cmd, pld, args: list[str]) -> discord.Embed:
    model = ' '.join(args) if args else None
    if model:
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_model', model)
        response = GenericResponse('The model has been updated.').ok()
    else:
        response = GenericResponse('The model has not been provided.').error()
    return response


async def set_directive(cmd, pld, args: list[str]) -> discord.Embed:
    directive = ' '.join(args) if args else None
    if directive:
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_directive', directive)
        response = GenericResponse('The directive has been updated.').ok()
    else:
        response = GenericResponse('The directive has not been provided.').error()
    return response


async def set_default(cmd, pld, _args) -> discord.Embed:
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_mode', None)
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_key', None)
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_endpoint', None)
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_model', None)
    await cmd.db.set_guild_settings(pld.msg.guild.id, 'cb_ai_directive', None)
    MESSAGE_STORE.update({pld.msg.guild.id: []})
    resp = GenericResponse('All AI settings have been set to default').ok()
    resp.description = 'If you would like to use an LLM without your own, just set the mode to custom and nothing else.'
    return resp


async def set_clean(_cmd, pld, _args) -> discord.Embed:
    MESSAGE_STORE.update({pld.msg.guild.id: []})
    return GenericResponse('Message history has been purged.').ok()


async def chatterbotset(cmd, pld):
    setter_funcs = {
        'mode': set_mode,
        'key': set_key,
        'endpoint': set_endpoint,
        'model': set_model,
        'directive': set_directive,
        'default': set_default,
        'clean': set_clean
    }
    modes = ', '.join([f'`{str(mode)}`' for mode in setter_funcs.keys()])
    is_owner = pld.msg.author.id in cmd.bot.cfg.dsc.owners
    is_manager = pld.msg.channel.permissions_for(pld.msg.author).manage_guild
    if is_owner or is_manager:
        if pld.args:
            setter_name = pld.args[0].lower()
            if setter_name in setter_funcs:
                subargs = pld.args[1:]
                setter_func = setter_funcs.get(setter_name)
                response = await setter_func(cmd, pld, subargs)
            else:
                response = GenericResponse(f'Unrecognized setter "{setter_name}" selected.').error()
                response.description = f'You can choose {modes}.'
        else:
            response = GenericResponse(
                'You didn\'t enter what you would like to set.'
            ).error()
            response.description = f'You can choose {modes}.'
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
