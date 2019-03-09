# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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
import secrets
import traceback

import discord

from sigma.core.mechanics.payload import CommandPayload, MessagePayload


class SigmaError(object):
    def __init__(self, cmd, exc: Exception):
        self.args = []
        self.data = {}
        self.db = cmd.db
        self.bot = cmd.bot
        self.log = cmd.log
        self.name = cmd.name
        self.exception = exc
        self.token = secrets.token_hex(16)
        self.icon_resp = cmd.respond_with_icon

    async def error_handler(self, pld: CommandPayload):
        self.args = pld.args
        self.data = self.make_error_dict(pld.msg)
        await self.icon_resp(pld.msg, '❗')
        await self.send_error_message(pld)
        await self.log_error()

    async def send_error_message(self, pld: MessagePayload):
        title, err_text = self.get_error_message(pld.settings)
        error_embed = discord.Embed(color=0xBE1931)
        error_embed.add_field(name=title, value=err_text)
        error_embed.set_footer(text=f'Token: {self.token}')
        try:
            await pld.msg.channel.send(embed=error_embed)
        except (discord.Forbidden, discord.NotFound):
            pass

    async def log_error(self):
        await self.db[self.db.db_nam].Errors.insert_one(self.data)
        log_text = f'ERROR: {self.exception} | TOKEN: {self.token} | TRACE: {self.exception.with_traceback}'
        self.log.error(log_text)

    def make_error_dict(self, message: discord.Message):
        gld = message.guild
        gnam = message.guild.name if gld else None
        gid = message.guild.id if gld else None
        cnam = message.channel.name if gld else None
        cid = message.channel.id if gld else None
        auth = f'{message.author.name}#{message.author.discriminator}'
        error_dict = {
            'token': self.token,
            'error': f'{self.exception}',
            'reported': False,
            'traceback': {
                'class': f'{self.exception.with_traceback}',
                'details': traceback.format_exc()
            },
            'message': {
                'command': self.name,
                'arguments': self.args,
                'id': message.id
            },
            'author': {
                'name': auth,
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

    @staticmethod
    def make_error_embed(error_file: dict):
        response = discord.Embed(color=0xBE1931, title=f'🚨 Error: `{error_file["token"]}`')
        cmd_text = f'Command: **{error_file["message"]["command"]}**'
        cmd_text += f'\nMessage ID: **{error_file["message"]["id"]}**'
        cmd_text += f'\nArguments: **{" ".join(error_file["message"]["arguments"][:200]) or "None"}**'
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

    def get_error_message(self, settings: dict):
        prefix = self.db.get_prefix(settings)
        # escapes markdown formatting
        prefix, name = list(map(lambda i: re.sub(r'([*_~`])', r'\\\1', i), [prefix, self.name]))
        if isinstance(self.exception, discord.Forbidden):
            title = '❗ Error: Forbidden!'
            err_text = f'It seems that you tried running something that {name} isn\'t allowed to'
            err_text += f'\ndo. This is something when {name} is missing permissions for stuff'
            err_text += '\nlike sending messages, adding reactions, uploading files, etc. The'
            err_text += '\nerror has been relayed to the developers. If you feel like dropping by'
            err_text += f'\nand asking about it, the invite link is in the **{prefix}help** command.'
        elif isinstance(self.exception, discord.NotFound):
            title = '❗ Error: Not Found!'
            err_text = 'It might have been a target that got removed while the command was'
            err_text += f'\nexecuting, whatever it was, {name} couldn\'t find it and encountered an'
            err_text += '\nerror. The error has been relayed to the developers. If you feel like'
            err_text += f'\ndropping by and asking about it, the invite link is in the **{prefix}help** command.'
        else:
            title = '❗ An Unhandled Error Occurred!'
            err_text = 'Something seems to have gone wrong.'
            err_text += '\nPlease be patient while we work on fixing the issue.'
            err_text += '\nThe error has been relayed to the developers.'
            err_text += '\nIf you feel like dropping by and asking about it,'
            err_text += f'\nthe invite link is in the **{prefix}help** command.'
        return title, err_text
