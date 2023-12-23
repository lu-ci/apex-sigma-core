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

import hashlib
import secrets

import aiohttp

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.tools.imgur import upload_image


def make_interaction_data(message, interaction_name, interaction_url, url_hash):
    """
    :type message: discord.Message
    :type interaction_name: str
    :type interaction_url: str
    :type url_hash: str
    :rtype: dict
    """
    return {
        'name': interaction_name.lower(),
        'user_id': message.author.id,
        'server_id': message.guild.id,
        'url': interaction_url,
        'hash': url_hash,
        'interaction_id': secrets.token_hex(4),
        'message_id': None,
        'reported': False,
        'active': False
    }


async def validate_gif_url(url):
    """
    :type url: str
    :rtype: bool, bytes
    """
    valid, data = False, None
    # noinspection PyBroadException
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_type = resp.headers.get('Content-Type') or resp.headers.get('content-type')
                valid = resp.status == 200 and resp_type == 'image/gif'
                if valid:
                    data = await resp.read()
    except Exception:
        pass
    return valid, data


def get_allowed_interactions(commands):
    """
    :type commands: dict
    :rtype: list
    """
    allowed_interactions = []
    for command in commands:
        command = commands.get(command)
        if command.category.lower() == 'interactions':
            if command.name != 'addinteraction':
                allowed_interactions.append(command.name)
    return allowed_interactions


async def relay_image(cmd, url):
    """
    :param cmd:
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type url: str
    :rtype: str
    """
    client_id = cmd.bot.modules.commands['imgur'].cfg.get('client_id')
    return await upload_image(url, client_id)


async def check_existence(db, data, name):
    """
    :type db: sigma.core.mechanics.database.Database
    :type data: bytes
    :type name: str
    :rtype: bool, str
    """
    url_hash = hash_url(data)
    exists = bool(await db.col.Interactions.find_one({'hash': url_hash, 'name': name}))
    return exists, url_hash


def hash_url(url):
    """
    :type url: bytes
    :rtype: str
    """
    crypt = hashlib.new('md5')
    crypt.update(url)
    return crypt.hexdigest()


async def addinteraction(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if 'client_id' in cmd.bot.modules.commands['imgur'].cfg:
        if pld.args:
            if len(pld.args) >= 2:
                interaction_name = pld.args[0].lower()
                interaction_link = ' '.join(pld.args[1:])
                allowed_interactions = get_allowed_interactions(cmd.bot.modules.commands)
                if interaction_name in allowed_interactions:
                    valid, data = await validate_gif_url(interaction_link)
                    if valid:
                        exists, url_hash = await check_existence(cmd.db, data, interaction_name)
                        if not exists:
                            if 'i.imgur.com' in interaction_link:
                                imgur_link = interaction_link
                            else:
                                imgur_link = await relay_image(cmd, interaction_link)
                            if imgur_link:
                                inter_data = make_interaction_data(pld.msg, interaction_name, imgur_link, url_hash)
                                if cmd.cfg.log_ch is None:
                                    inter_data.update({'active': True})
                                await cmd.db.col.Interactions.insert_one(inter_data)
                                title = f'Interaction {interaction_name} {inter_data.get("interaction_id")} submitted.'
                                response = GenericResponse(title).ok()
                            else:
                                response = GenericResponse('Bad GIF.').error()
                        else:
                            response = GenericResponse('That GIF has already been submitted.').error()
                    else:
                        response = GenericResponse('The submitted link gave a bad response.').error()
                else:
                    response = GenericResponse('No such interaction was found.').error()
            else:
                response = GenericResponse('Not enough arguments.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await pld.msg.channel.send(embed=response)
