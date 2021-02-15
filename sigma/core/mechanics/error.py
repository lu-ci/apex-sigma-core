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

import secrets
import traceback

import discord


class SigmaError(object):
    """
    This class contains error processing methods.
    """

    __slots__ = ("args", "data", "cmd", "exception", "token")

    def __init__(self, cmd, exc):
        """
        :param cmd: The command instance generating the error.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        :type exc: Exception
        """
        self.args = []
        self.data = {}
        self.cmd = cmd
        self.exception = exc
        self.token = secrets.token_hex(16)

    async def error_handler(self, pld):
        """
        Processes an error that happened during a command's execution.
        :param pld: The command's payload data.
        :type pld: sigma.core.mechanics.payload.CommandPayload
        """
        self.args = pld.args
        self.data = self.make_error_dict(pld.msg)
        await self.cmd.respond_with_emote(pld.msg, '❗')
        await self.send_error_message(pld)
        await self.log_error()

    async def send_error_message(self, pld):
        """
        Sends an error embed with an explanation to the
        channel where the command broke.
        :param pld: The command's payload data.
        :type pld: sigma.core.mechanics.payload.CommandPayload
        """
        title, err_text = self.get_error_message(pld.settings)
        error_embed = discord.Embed(color=0xBE1931)
        error_embed.add_field(name=title, value=err_text)
        error_embed.set_footer(text=f'Token: {self.token}')
        try:
            await pld.msg.channel.send(embed=error_embed)
        except (discord.Forbidden, discord.NotFound):
            pass

    async def log_error(self):
        """
        Adds a line to the logger with the error information.
        Also adds the error data to the database.
        """
        await self.cmd.db[self.cmd.db.db_nam].Errors.insert_one(self.data)
        log_text = f'ERROR: {self.exception} | TOKEN: {self.token} | TRACE: {self.exception.with_traceback}'
        self.cmd.log.error(log_text)

    def make_error_dict(self, message):
        """
        Constructs the dict data of the error
        to be stored in the database.
        :type message: discord.Message
        :rtype: dict
        """
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
                'command': self.cmd.name,
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
    def make_error_embed(error_file):
        """
        Constructs the embed with the error's details
        to report back to the owner's error log channel.
        :type error_file: dict
        :rtype: discord.Embed, str
        """
        response = discord.Embed(color=0xBE1931, title=f'🚨 Error: `{error_file["token"]}`')
        cmd_text = f'Command: **{error_file["message"]["command"]}**'
        cmd_text += f'\nMessage ID: **{error_file["message"]["id"]}**'
        cmd_text += f'\nArguments: **{" ".join(error_file["message"]["arguments"][:10]) or "None"}**'
        orgn_text = f'Author: **{error_file["author"]["name"]}**'
        orgn_text += f'\nAuthor ID: **{error_file["author"]["id"]}**'
        orgn_text += f'\nChannel: **{error_file["channel"]["name"]}**'
        orgn_text += f'\nChannel ID: **{error_file["channel"]["id"]}**'
        orgn_text += f'\nGuild: **{error_file["guild"]["name"]}**'
        orgn_text += f'\nGuild ID: **{error_file["guild"]["id"]}**'
        trace_text = f'Trace Class:\n**{error_file["traceback"]["class"]}**'
        trace_text += f'\nTrace Details:\n```py\n{error_file["traceback"]["details"][:800]}\n```'
        response.add_field(name='Command', value=cmd_text)
        response.add_field(name='Origin', value=orgn_text)
        return response, trace_text

    def get_error_message(self, settings):
        """
        Generates a message to show to the users
        that were affected by the command breaking.
        :type settings: dict
        :rtype: str, str
        """
        prefix = self.cmd.db.get_prefix(settings)
        # escapes markdown formatting
        name = self.cmd.name
        for escapable in '*_~`':
            prefix = prefix.replace(escapable, f'\\{escapable}')
        if isinstance(self.exception, discord.Forbidden):
            title = '❗ Error: Forbidden!'
            err_text = f'It seems that you tried running something that {name} isn\'t allowed to'
            err_text += f' do. This is something when {name} is missing permissions for stuff'
            err_text += ' like sending messages, adding reactions, uploading files, etc. The'
            err_text += ' error has been relayed to the developers. If you feel like dropping by'
            err_text += f' and asking about it, the invite link is in the **{prefix}help** command.'
        elif isinstance(self.exception, discord.NotFound):
            title = '❗ Error: Not Found!'
            err_text = 'It might have been a target that got removed while the command was'
            err_text += f' executing, whatever it was, {name} couldn\'t find it and encountered an'
            err_text += ' error. The error has been relayed to the developers. If you feel like'
            err_text += f' dropping by and asking about it, the invite link is in the **{prefix}help** command.'
        elif isinstance(self.exception, discord.HTTPException):
            title = '❗ Error: Connection Issue!'
            err_text = 'This is a general connectivity error which occurs if Discord suddenly drops the connection.'
            err_text += ' The reasons can vary from a simple hiccup in the pipeline to the gateway being under heavy'
            err_text += ' load. Regardless, if you notice these occurring too frequently, you can always'
            err_text += f' drop by and ask about it, the invite link is in the **{prefix}help** command.'
        else:
            title = '❗ An Unhandled Error Occurred!'
            err_text = 'Something seems to have gone wrong.'
            err_text += ' Please be patient while we work on fixing the issue.'
            err_text += ' The error has been relayed to the developers.'
            err_text += ' If you feel like dropping by and asking about it,'
            err_text += f' the invite link is in the **{prefix}help** command.'
        return title, err_text
