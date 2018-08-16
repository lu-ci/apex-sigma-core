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

import traceback
import re

import discord


def make_error_dict(message: discord.Message, exception: Exception, token: str, args: list, name: str):
    gld = message.guild
    gnam = message.guild.name if gld else None
    gid = message.guild.id if gld else None
    cnam = message.channel.name if gld else None
    cid = message.channel.id if gld else None
    error_dict = {
        'token': token,
        'error': f'{exception}',
        'traceback': {
            'class': f'{exception.with_traceback}',
            'details': traceback.format_exc()
        },
        'message': {
            'command': name,
            'arguments': args,
            'id': message.id
        },
        'author': {
            'name': f'{message.author.name}#{message.author.discriminator}',
            'id': message.author.id
        },
        'guild': {
            'name': gnam,
            'id': gid
        },
        'channel': {
            'name': cnam,
            'id': cid
        }
    }
    return error_dict


def get_error_message(error: Exception, name: str, prefix: str):
    prefix = re.sub(r'([*_~`])', r'\\\1', prefix)
    if isinstance(error, discord.Forbidden):
        title = '❗ Error: Forbidden!'
        err_text = f'It seems that you tried running something that {name} isn\'t allowed to do.'
        err_text += f' This is something when {name} is missing permissions for stuff like'
        err_text += ' sending messages, adding reactions, uploading files, etc.'
        err_text += ' The error has been relayed to the developers. If you feel like dropping by'
        err_text += f' and asking about it, the invite link is in the **{prefix}help** command.'
    elif isinstance(error, discord.NotFound):
        title = '❗ Error: Not Found!'
        err_text = 'It might have been a target that got removed while the command was executing,'
        err_text += f' whatever it was, {name} couldn\'t find it and encountered an error.'
        err_text += ' The error has been relayed to the developers. If you feel like dropping by'
        err_text += f' and asking about it, the invite link is in the **{prefix}help** command.'
    else:
        title = '❗ An Unhandled Error Occurred!'
        err_text = 'Something seems to have gone wrong.'
        err_text += '\nPlease be patient while we work on fixing the issue.'
        err_text += '\nThe error has been relayed to the developers.'
        err_text += f'\nIf you feel like dropping by and asking about it,'
        err_text += f'\nthe invite link is in the **{prefix}help** command.'
    return title, err_text


async def make_error_embed(error_file):
    response = discord.Embed(color=0xBE1931, title=f'🚨 Error: `{error_file["token"]}`')
    cmd_text = f'Command: **{error_file["message"]["command"]}**'
    cmd_text += f'\nID: **{error_file["message"]["id"]}**'
    cmd_text += f'\nArguments: **{" ".join(error_file["message"]["arguments"]) or "None"}**'
    orgn_text = f'Author: **{error_file["author"]["name"]}**'
    orgn_text += f'\nAuthor ID: **{error_file["author"]["id"]}**'
    orgn_text += f'\nChannel: **{error_file["channel"]["name"]}**'
    orgn_text += f'\nChannel ID: **{error_file["channel"]["id"]}**'
    orgn_text += f'\nGuild: **{error_file["guild"]["name"]}**'
    orgn_text += f'\nGuild ID: **{error_file["guild"]["id"]}**'
    trace_text = f'Trace Class:\n**{error_file["traceback"]["class"]}**'
    trace_text += f'\nTrace Details:\n```py\n{error_file["traceback"]["details"][:1800]}\n```'
    response.add_field(name='Command', value=cmd_text)
    response.add_field(name='Origin', value=orgn_text)
    return response, trace_text


async def send_error_embed(error_chn, error_data):
    if error_chn:
        response, trace = await make_error_embed(error_data)
        await error_chn.send(embed=response)
        if trace:
            await error_chn.send(trace)
