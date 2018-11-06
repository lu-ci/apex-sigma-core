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

import hashlib
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.utilities.tools.imgur import upload_image


async def send_log_message(cmd: SigmaCommand, message: discord.Message, inter_data: dict):
    log_ch_id = cmd.cfg.get('log_ch')
    interact_log_ch = None
    if log_ch_id:
        interact_log_ch = await cmd.bot.get_channel(log_ch_id, True)
    if interact_log_ch:
        interaction_url = inter_data.get('url')
        interaction_id = inter_data.get('interaction_id')
        interaction_name = inter_data.get('name')
        author = f'{message.author.name}#{message.author.discriminator}'
        data_desc = f'Author: {author}'
        data_desc += f'\nAuthor ID: {message.author.id}'
        data_desc += f'\nGuild: {message.guild.name}'
        data_desc += f'\nGuild ID: {message.guild.id}'
        data_desc += f'\nInteraction URL: [Here]({interaction_url})'
        data_desc += f'\nInteraction ID: {interaction_id}'
        log_resp_title = f'🆙 Added a new {interaction_name.lower()}'
        log_resp = discord.Embed(color=0x3B88C3)
        log_resp.add_field(name=log_resp_title, value=data_desc)
        log_resp.set_thumbnail(url=interaction_url)
        log_msg = await interact_log_ch.send(embed=log_resp)
        return log_msg


def make_interaction_data(message: discord.Message, interaction_name: str, interaction_url: str, url_hash: str):
    return {
        'name': interaction_name.lower(),
        'user_id': message.author.id,
        'server_id': message.guild.id,
        'url': interaction_url,
        'hash': url_hash,
        'interaction_id': secrets.token_hex(4),
        'message_id': None
    }


async def validate_gif_url(url: str):
    valid, data = False, None
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


def get_allowed_interactions(commands: dict):
    allowed_interactions = []
    for command in commands:
        command = commands.get(command)
        if command.category.lower() == 'interactions':
            if command.name not in ['addinteraction', 'lovecalculator']:
                allowed_interactions.append(command.name)
    return allowed_interactions


async def relay_image(cmd: SigmaCommand, url: str):
    client_id = cmd.bot.modules.commands['imgur'].cfg.get('client_id')
    return await upload_image(url, client_id)


async def check_existence(db: Database, data: bytes, name: str):
    url_hash = hash_url(data)
    exists = bool(await db[db.db_nam].Interactions.find_one({'hash': url_hash, 'name': name}))
    return exists, url_hash


def hash_url(url: bytes):
    crypt = hashlib.new('md5')
    crypt.update(url)
    return crypt.hexdigest()


async def addinteraction(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        if len(args) >= 2:
            interaction_name = args[0].lower()
            interaction_link = ' '.join(args[1:])
            allowed_interactions = get_allowed_interactions(cmd.bot.modules.commands)
            if interaction_name in allowed_interactions:
                valid, data = await validate_gif_url(interaction_link)
                if valid:
                    exists, url_hash = await check_existence(cmd.db, data, interaction_name)
                    if not exists:
                        imgur_link = await relay_image(cmd, interaction_link)
                        if imgur_link:
                            inter_data = make_interaction_data(message, interaction_name, imgur_link, url_hash)
                            log_msg = await send_log_message(cmd, message, inter_data)
                            inter_data.update({'message_id': log_msg.id if log_msg else None})
                            await cmd.db[cmd.db.db_nam].Interactions.insert_one(inter_data)
                            title = f'✅ Interaction {interaction_name} {inter_data.get("interaction_id")} submitted.'
                            response = discord.Embed(color=0x77B255, title=title)
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ Bad GIF.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ That GIF has already been submitted.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ The submitted link gave a bad response.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ No such interaction was found.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputted.')
    await message.channel.send(embed=response)
