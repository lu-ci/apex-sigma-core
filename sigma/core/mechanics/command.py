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

import os
import secrets
import traceback

import arrow
import discord
import yaml

from sigma.core.mechanics.cooldown import CommandRateLimiter
from sigma.core.mechanics.exceptions import DummyException
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.mechanics.permissions import ServerCommandPermissions
from sigma.core.mechanics.requirements import CommandRequirements
from sigma.core.utilities.stats_processing import add_cmd_stat
from sigma.modules.owner_controls.core.error_parser import send_error_embed


class SigmaCommand(object):
    def __init__(self, bot, command, plugin_info, command_info):
        self.bot = bot
        self.db = self.bot.db
        self.cd = CommandRateLimiter(self)
        self.command = command
        self.plugin_info = plugin_info
        self.command_info = command_info
        self.name = self.command_info.get('name')
        self.path = self.command_info.get('path')
        self.category = self.plugin_info.get('category')
        self.subcategory = self.plugin_info.get('subcategory')
        self.log = create_logger(self.name.upper())
        self.nsfw = False
        self.cfg = {}
        self.cache = {}
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = ['send_messages', 'embed_links']
        self.alts = []
        self.usage = '{pfx}{cmd}'
        self.desc = 'No description provided.'
        self.insert_command_info()
        self.load_command_config()

    @staticmethod
    def get_usr_data(usr: discord.User):
        usr_data = {
            'color': str(usr.color) if isinstance(usr, discord.Member) else '#000000',
            'created': str(usr.created_at),
            'discriminator': usr.discriminator,
            'display_name': usr.display_name,
            'game': (usr.activity.name if usr.activity else None) if isinstance(usr, discord.Member) else None,
            'id': usr.id,
            'name': usr.name,
            'status': str(usr.status) if isinstance(usr, discord.Member) else None
        }
        return usr_data

    def insert_command_info(self):
        self.alts = self.command_info.get('alts', [])
        self.usage = self.command_info.get('usage', '{pfx}{cmd}')
        self.desc = self.command_info.get('description', 'No description provided.')
        self.requirements += self.command_info.get('requirements', [])
        permissions = self.command_info.get('permissions', {})
        if permissions:
            self.nsfw = bool(permissions.get('nsfw'))
            self.owner = bool(permissions.get('owner'))
            self.partner = bool(permissions.get('partner'))
            self.dmable = bool(permissions.get('dmable'))
        if self.owner:
            self.desc += '\n(Bot Owner Only)'

    def load_command_config(self):
        config_path = f'config/plugins/{self.name}.yml'
        if os.path.exists(config_path):
            with open(config_path) as config_file:
                self.cfg = yaml.safe_load(config_file)

    def resource(self, res_path: str):
        module_path = self.path
        res_path = f'{module_path}/res/{res_path}'
        res_path = res_path.replace('\\', '/')
        return res_path

    def get_exception(self):
        if self.bot.cfg.pref.dev_mode:
            cmd_exception = DummyException
        else:
            cmd_exception = Exception
        return cmd_exception

    def log_command_usage(self, message: discord.Message, args: list, extime: int):
        crst = arrow.get(message.created_at).float_timestamp
        exdiff = round(extime - crst, 3)
        if message.guild:
            cmd_location = f'SRV: {message.guild.name} [{message.guild.id}] | '
            cmd_location += f'CHN: #{message.channel.name} [{message.channel.id}]'
        else:
            cmd_location = 'DIRECT MESSAGE'
        author_full = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
        log_text = f'USR: {author_full} | {cmd_location}'
        if args:
            log_text += f' | ARGS: {" ".join(args)}'
        log_text += f' | EX: {exdiff}'
        self.log.info(log_text)

    async def add_usage_exp(self, message: discord.Message):
        if message.guild:
            if not await self.bot.cool_down.on_cooldown('UsageExperience', message.author):
                award_xp = (600 if message.guild.large else 500) + secrets.randbelow(100)
                await self.db.add_experience(message.author, message.guild, award_xp)
                await self.bot.cool_down.set_cooldown('UsageExperience', message.author, 450)

    @staticmethod
    async def respond_with_icon(message: discord.Message, icon: str or discord.Emoji):
        try:
            await message.add_reaction(icon)
        except discord.DiscordException:
            pass

    async def log_error(self, message: discord.Message, args: list, exception: Exception, error_token: str):
        if message.guild:
            gnam = message.guild.name
            gid = message.guild.id
            cnam = message.channel.name
            cid = message.channel.id
        else:
            gnam = None
            gid = None
            cnam = None
            cid = None
        err_file_data = {
            'token': error_token,
            'error': f'{exception}',
            'traceback': {
                'class': f'{exception.with_traceback}',
                'details': traceback.format_exc()
            },
            'message': {
                'command': self.name,
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
        if self.bot.cfg.pref.errorlog_channel:
            err_chn_id = self.bot.cfg.pref.errorlog_channel
            error_chn = discord.utils.find(lambda x: x.id == err_chn_id, self.bot.get_all_channels())
            await send_error_embed(error_chn, err_file_data)
        await self.db[self.bot.cfg.db.database].Errors.insert_one(err_file_data)
        log_text = f'ERROR: {exception} | TOKEN: {error_token} | TRACE: {exception.with_traceback}'
        self.log.error(log_text)

    async def send_error_message(self, message: discord.Message, args: list, e: Exception):
        await self.respond_with_icon(message, '❗')
        err_token = secrets.token_hex(16)
        await self.log_error(message, args, e, err_token)
        prefix = await self.db.get_prefix(message)
        name = self.bot.user.name
        if isinstance(e, discord.Forbidden):
            title = '❗ Error: Forbidden!'
            err_text = f'It seems that you tried running something that {name} isn\'t allowed to do.'
            err_text += f' This is something when {name} is missing permissions for stuff like'
            err_text += ' sending messages, adding reactions, uploading files, etc.'
            err_text += ' The error has been relayed to the developers. If you feel like dropping by'
            err_text += f' and asking about it, the invite link is in the **{prefix}help** command.'
        elif isinstance(e, discord.NotFound):
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
        error_embed = discord.Embed(color=0xBE1931)
        error_embed.add_field(name=title, value=err_text)
        error_embed.set_footer(text=f'Token: {err_token}')
        try:
            await message.channel.send(embed=error_embed)
        except (discord.Forbidden, discord.NotFound):
            pass

    async def update_cooldown(self, author):
        cdfile = await self.db[self.db.db_nam].CommandCooldowns.find_one({'command': self.name}) or {}
        cooldown = cdfile.get('cooldown')
        if cooldown:
            await self.bot.cool_down.set_cooldown(f'{self.name}_core', author, cooldown)

    async def execute(self, message: discord.Message, args: list):
        if self.bot.ready:
            if message.guild:
                delete_command_message = await self.db.get_guild_settings(message.guild.id, 'DeleteCommands')
                if delete_command_message:
                    try:
                        await message.delete()
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
            if not self.bot.cfg.dsc.bot and message.author.id != self.bot.user.id:
                self.log.warning(f'{message.author.name} tried using me.')
                return
            if not self.cd.is_cooling(message):
                if not await self.bot.cool_down.on_cooldown(f'{self.name}_core', message.author):
                    await self.update_cooldown(message.author)
                    perms = GlobalCommandPermissions(self, message)
                    await perms.check_black_usr()
                    await perms.check_black_srv()
                    await perms.generate_response()
                    perms.check_final()
                    guild_allowed = ServerCommandPermissions(self, message)
                    await guild_allowed.check_perms()
                    self.log_command_usage(message, args, arrow.utcnow().float_timestamp)
                    self.cd.set_cooling(message)
                    if perms.permitted:
                        if guild_allowed.permitted:
                            requirements = CommandRequirements(self, message)
                            if requirements.reqs_met:
                                try:
                                    await getattr(self.command, self.name)(self, message, args)
                                    await add_cmd_stat(self)
                                    await self.add_usage_exp(message)
                                    self.bot.command_count += 1
                                    event_task = self.bot.queue.event_runner('command', self, message, args)
                                    self.bot.loop.create_task(event_task)
                                except self.get_exception() as e:
                                    await self.send_error_message(message, args, e)

                            else:
                                await self.respond_with_icon(message, '📝')
                                reqs_embed = discord.Embed(color=0xBE1931)
                                reqs_error_title = f'❗ {self.bot.user.name} is missing permissions!'
                                reqs_error_list = ''
                                for req in requirements.missing_list:
                                    req = req.replace('_', ' ').title()
                                    reqs_error_list += f'\n- {req}'
                                prefix = await self.db.get_prefix(message)
                                reqs_embed.add_field(name=reqs_error_title, value=f'```\n{reqs_error_list}\n```')
                                reqs_embed.set_footer(text=f'{prefix}{self.name} could not execute.')
                                try:
                                    await message.channel.send(embed=reqs_embed)
                                except (discord.Forbidden, discord.NotFound):
                                    pass
                        else:
                            self.log.warning('ACCESS DENIED: This module or command is not allowed in this location.')
                            await self.respond_with_icon(message, '🔒')
                    else:
                        perms.log_unpermitted()
                        await self.respond_with_icon(message, '⛔')
                        if perms.response:
                            try:
                                await message.channel.send(embed=perms.response)
                            except discord.Forbidden:
                                pass
                else:
                    await self.respond_with_icon(message, '❄')
            else:
                await self.respond_with_icon(message, '🕙')
