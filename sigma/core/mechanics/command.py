import os
import secrets
import traceback

import arrow
import discord
import yaml

from sigma.core.mechanics.command_requirements import CommandRequirements
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.mechanics.permissions import ServerCommandPermissions
from sigma.core.utilities.stats_processing import add_cmd_stat


class SigmaCommand(object):
    def __init__(self, bot, command, plugin_info, command_info):
        self.bot = bot
        self.db = self.bot.db
        self.command = command
        self.plugin_info = plugin_info
        self.command_info = command_info
        self.name = self.command_info['name']
        self.path = self.command_info['path']
        self.category = self.plugin_info['category']
        self.log = create_logger(self.name.upper())
        self.nsfw = False
        self.cfg = {}
        self.cache = {}
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = ['send_messages', 'embed_links']
        self.alts = None
        self.usage = f'{bot.cfg.pref.prefix}{self.name}'
        self.desc = 'No description provided.'
        self.insert_command_info()
        self.load_command_config()

    def insert_command_info(self):
        if 'alts' in self.command_info:
            self.alts = self.command_info['alts']
        if 'usage' in self.command_info:
            self.usage = self.command_info['usage']
            self.usage = self.usage.replace('{pfx}', self.bot.cfg.pref.prefix)
            self.usage = self.usage.replace('{cmd}', self.name)
        if 'description' in self.command_info:
            self.desc = self.command_info['description']
        if 'requirements' in self.command_info:
            self.requirements += self.command_info['requirements']
        if 'permissions' in self.command_info:
            permissions = self.command_info['permissions']
            if 'nsfw' in permissions:
                self.nsfw = permissions['nsfw']
            if 'owner' in permissions:
                self.owner = permissions['owner']
            if 'partner' in permissions:
                self.partner = permissions['partner']
            if 'dmable' in permissions:
                self.dmable = permissions['dmable']
        if self.owner:
            self.desc += '\n(Bot Owner Only)'

    def load_command_config(self):
        config_path = f'config/plugins/{self.name}.yml'
        if os.path.exists(config_path):
            with open(config_path) as config_file:
                self.cfg = yaml.safe_load(config_file)

    def resource(self, res_path):
        module_path = self.path
        res_path = f'{module_path}/res/{res_path}'
        res_path = res_path.replace('\\', '/')
        return res_path

    def get_exception(self):
        if self.bot.cfg.pref.dev_mode:
            cmd_exception = SyntaxError
        else:
            cmd_exception = Exception
        return cmd_exception

    def log_command_usage(self, message, args):
        if message.guild:
            cmd_location = f'SRV: {message.guild.name} [{message.guild.id}] | '
            cmd_location += f'CHN: #{message.channel.name} [{message.channel.id}]'
        else:
            cmd_location = 'DIRECT MESSAGE'
        author_full = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
        log_text = f'USR: {author_full} | {cmd_location}'
        if args:
            log_text += f' | ARGS: {" ".join(args)}'
        self.log.info(log_text)

    def log_unpermitted(self, perms):
        log_text = f'ACCESS DENIED | '
        log_text += f'BUSR: {perms.black_user} | MDL: {perms.module_denied} | BSRV: {perms.black_srv} | '
        log_text += f'OWNR: {perms.owner_denied} | DM: {perms.dm_denied} | NSFW: {perms.nsfw_denied} | '
        log_text += f'VIP: {perms.partner_denied}'
        self.log.warning(log_text)

    def add_usage_exp(self, message):
        if message.guild:
            if not self.bot.cool_down.on_cooldown('UsageExperience', message.author):
                exp_points = 1 + secrets.randbelow(9)
                self.db.add_experience(message.author, message.guild, exp_points)
                self.bot.cool_down.set_cooldown('UsageExperience', message.author, 30)

    @staticmethod
    async def respond_with_icon(message, icon):
        try:
            await message.add_reaction(icon)
        except discord.DiscordException:
            pass

    def log_error(self, message, args, exception, error_token):
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
            'Token': error_token,
            'Error': f'{exception}',
            'TraceBack': {
                'Class': f'{exception.with_traceback}',
                'Details': traceback.format_exc()
            },
            'Message': {
                'Command': self.name,
                'Arguments': args,
                'ID': message.id
            },
            'Author': {
                'Name': f'{message.author.name}#{message.author.discriminator}',
                'ID': message.author.id
            },
            'Guild': {
                'Name': gnam,
                'ID': gid
            },
            'Channel': {
                'Name': cnam,
                'ID': cid
            }
        }
        self.db[self.bot.cfg.db.database].Errors.insert_one(err_file_data)
        log_text = f'ERROR: {exception} | TOKEN: {error_token} | TRACE: {exception.with_traceback}'
        self.log.error(log_text)

    async def execute(self, message, args):
        start_stamp = arrow.utcnow().float_timestamp
        if self.bot.ready:
            if message.guild:
                delete_command_message = self.db.get_guild_settings(message.guild.id, 'DeleteCommands')
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
            cd_identifier = f'{self.name}_{message.author.id}'
            if not self.bot.cool_down.cmd.on_cooldown(cd_identifier):
                self.bot.cool_down.cmd.set_cooldown(cd_identifier)
                perms = GlobalCommandPermissions(self, message)
                guild_allowed = ServerCommandPermissions(self, message)
                self.log_command_usage(message, args)
                if perms.permitted:
                    if guild_allowed.permitted:
                        requirements = CommandRequirements(self, message)
                        if requirements.reqs_met:
                            try:
                                await getattr(self.command, self.name)(self, message, args)
                                await add_cmd_stat(self.db, self, message, args)
                                self.add_usage_exp(message)
                                self.bot.command_count += 1
                            except self.get_exception() as e:
                                await self.respond_with_icon(message, '❗')
                                err_token = secrets.token_hex(16)
                                self.log_error(message, args, e, err_token)
                                prefix = self.bot.get_prefix(message)
                                title = '❗ An Error Occurred!'
                                err_text = 'Something seems to have gone wrong.'
                                err_text += '\nPlease send this token to our support server.'
                                err_text += f'\nThe invite link is in the **{prefix}help** command.'
                                err_text += f'\nToken: **{err_token}**'
                                error_embed = discord.Embed(color=0xBE1931)
                                error_embed.add_field(name=title, value=err_text)
                                try:
                                    await message.channel.send(embed=error_embed)
                                except discord.Forbidden:
                                    pass
                        else:
                            await self.respond_with_icon(message, '❗')
                            reqs_embed = discord.Embed(color=0xBE1931)
                            reqs_error_title = f'❗ I am missing permissions!'
                            reqs_error_list = ''
                            for req in requirements.missing_list:
                                req = req.replace('_', ' ').title()
                                reqs_error_list += f'\n- {req}'
                            reqs_embed.add_field(name=reqs_error_title, value=f'```\n{reqs_error_list}\n```')
                            reqs_embed.set_footer(text=f'{self.bot.get_prefix(message)}{self.name}')
                            try:
                                await message.channel.send(embed=reqs_embed)
                            except discord.Forbidden:
                                pass
                    else:
                        self.log.warning('ACCESS DENIED: This module or command is not allowed in this location.')
                        await self.respond_with_icon(message, '⛔')
                else:
                    self.log_unpermitted(perms)
                    await self.respond_with_icon(message, '⛔')
                    if perms.response:
                        try:
                            await message.channel.send(embed=perms.response)
                        except discord.Forbidden:
                            pass
            else:
                await self.respond_with_icon(message, '🕦')
        end_stamp = arrow.utcnow().float_timestamp
        diff = round(end_stamp - start_stamp, 5)
        exec_time = f'{self.name} Execution time: {diff}s'
        if diff < 5:
            self.log.debug(exec_time)
        else:
            self.log.warning(exec_time)
