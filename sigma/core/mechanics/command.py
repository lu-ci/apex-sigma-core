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

import os
import secrets

import arrow
import discord
import yaml

from sigma.core.mechanics.config import ModuleConfig
from sigma.core.mechanics.cooldown import CommandRateLimiter
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.errors import SigmaError
from sigma.core.mechanics.exceptions import DummyException
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.payload import CommandEventPayload, CommandPayload
from sigma.core.mechanics.permissions import GlobalCommandPermissions, ServerCommandPermissions, check_filter_perms
from sigma.core.mechanics.requirements import CommandRequirements
from sigma.core.utilities.stats_processing import add_cmd_stat


class SigmaCommand(object):
    def __init__(self, bot, command, module_info: dict, command_info: dict):
        self.bot = bot
        self.db: Database = self.bot.db
        self.cd = CommandRateLimiter(self)
        self.command = command
        self.module_info = module_info
        self.command_info = command_info
        self.name = self.command_info.get('name')
        self.path = self.command_info.get('path')
        self.category = self.module_info.get('category')
        self.subcategory = self.module_info.get('subcategory')
        self.log = create_logger(self.name.upper(), shard=self.bot.cfg.dsc.shard)
        self.nsfw = False
        self.cfg = ModuleConfig(self)
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = ['send_messages', 'embed_links']
        self.alts = []
        self.usage = '{pfx}{cmd}'
        self.desc = 'No description provided.'
        self.insert_command_info()
        self.load_command_config()

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
        config_path = f'config/modules/{self.name}.yml'
        if os.path.exists(config_path):
            with open(config_path) as config_file:
                self.cfg.load(yaml.safe_load(config_file))

    def resource(self, res_path: str):
        module_path = self.path
        res_path = f'{module_path}/res/{res_path}'
        res_path = res_path.replace('\\', '/')
        return res_path

    def get_exception(self):
        return DummyException if self.bot.cfg.pref.dev_mode else Exception

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

    async def add_usage_sum(self, message: discord.Message):
        trigger = f'usage_{self.name}'
        if message.guild and not await self.bot.cool_down.on_cooldown(trigger, message.author):
            await self.bot.cool_down.set_cooldown(trigger, message.author, 450)
            award = secrets.randbelow(3)
            if award:
                await self.db.add_resource(message.author.id, 'sumarum', award, trigger, message, True)

    @staticmethod
    async def respond_with_icon(message: discord.Message, icon: str or discord.Emoji):
        try:
            await message.add_reaction(icon)
        except discord.DiscordException:
            pass

    async def update_cooldown(self, author):
        cdfile = await self.db[self.db.db_nam].CommandCooldowns.find_one({'command': self.name}) or {}
        cooldown = cdfile.get('cooldown')
        if cooldown:
            await self.bot.cool_down.set_cooldown(f'{self.name}_core', author, cooldown)

    @staticmethod
    async def check_black_args(settings: dict, args: list):
        black_args = settings.get('blocked_args', [])
        trigg_args = [arg for arg in args if arg in black_args]
        return any(trigg_args)

    async def execute(self, payload: CommandPayload):
        if self.bot.ready:
            if payload.msg.guild:
                delete_command_message = payload.settings.get('delete_commands')
                if delete_command_message:
                    try:
                        await payload.msg.delete()
                    except (discord.Forbidden, discord.NotFound):
                        pass
                override = check_filter_perms(payload.msg, payload.settings, 'arguments')
                if await self.check_black_args(payload.settings, payload.args):
                    if not any([payload.msg.author.guild_permissions.administrator, override]):
                        await self.respond_with_icon(payload.msg, '🛡')
                        return
            if not self.bot.cfg.dsc.bot and payload.msg.author.id != self.bot.user.id:
                self.log.warning(f'{payload.msg.author.name} tried using me.')
                return
            if not self.cd.is_cooling(payload.msg):
                if not await self.bot.cool_down.on_cooldown(f'{self.name}_core', payload.msg.author):
                    await self.update_cooldown(payload.msg.author)
                    perms = GlobalCommandPermissions(self, payload)
                    await perms.check_black_usr()
                    await perms.check_black_srv()
                    perms.generate_response()
                    perms.check_final()
                    guild_allowed = ServerCommandPermissions(self, payload.msg)
                    await guild_allowed.check_perms()
                    self.log_command_usage(payload.msg, payload.args, arrow.utcnow().float_timestamp)
                    self.cd.set_cooling(payload.msg)
                    if perms.permitted:
                        if guild_allowed.permitted:
                            requirements = CommandRequirements(self, payload.msg)
                            if requirements.reqs_met:
                                try:
                                    await getattr(self.command, self.name)(self, payload)
                                    await add_cmd_stat(self)
                                    await self.add_usage_sum(payload.msg)
                                    self.bot.command_count += 1
                                    cmd_ev_pld = CommandEventPayload(self.bot, self, payload)
                                    event_task = self.bot.queue.event_runner('command', cmd_ev_pld)
                                    self.bot.loop.create_task(event_task)
                                except self.get_exception() as e:
                                    error = SigmaError(self, e)
                                    await error.error_handler(payload)
                            else:
                                await self.respond_with_icon(payload.msg, '📝')
                                reqs_embed = discord.Embed(color=0xBE1931)
                                reqs_error_title = f'❗ {self.bot.user.name} is missing permissions!'
                                reqs_error_list = ''
                                for req in requirements.missing_list:
                                    req = req.replace('_', ' ').title()
                                    reqs_error_list += f'\n- {req}'
                                prefix = self.db.get_prefix(payload.settings)
                                reqs_embed.add_field(name=reqs_error_title, value=f'```\n{reqs_error_list}\n```')
                                reqs_embed.set_footer(text=f'{prefix}{self.name} could not execute.')
                                try:
                                    await payload.msg.channel.send(embed=reqs_embed)
                                except (discord.Forbidden, discord.NotFound):
                                    pass
                        else:
                            self.log.warning('ACCESS DENIED: This module or command is not allowed in this location.')
                            await self.respond_with_icon(payload.msg, '🔒')
                    else:
                        perms.log_unpermitted()
                        await self.respond_with_icon(payload.msg, '⛔')
                        if perms.response:
                            try:
                                await payload.msg.channel.send(embed=perms.response)
                            except (discord.Forbidden, discord.NotFound):
                                pass
                else:
                    await self.respond_with_icon(payload.msg, '❄')
            else:
                await self.respond_with_icon(payload.msg, '🕙')
