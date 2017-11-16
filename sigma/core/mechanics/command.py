import os
import secrets
import traceback
import inspect

import discord

from sigma.core.mechanics.module_component import SigmaModuleComponent
from sigma.core.mechanics.command_requirements import CommandRequirements
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.mechanics.permissions import ServerCommandPermissions
from sigma.core.utilities.stats_processing import add_cmd_stat

class SigmaCommand(SigmaModuleComponent):
    """
    Represents a Sigma Discord command.

    Parameters
    ----------
    module: SigmaModule
        The module this command belongs to.
    config: dict
        Command configuration.

    Attributes
    ----------
    usage: string
        The command usage help message.
        {pfx} and {cmd} will be replaced by prefix and
        command name respectively.
    desc: string
        Short description of the command's functionality.
    alts: list(string)
        List of aliases for this command.
    requirements: list(string)
        List of required permissions to use this command.
    """
    def __init__(self, module, config):
        super().__init__(module, config)

        self.log = create_logger(self.name.upper())
        self.module = module
        self.cfg = {}
        self.cache = {}

    @property
    def usage(self):
        usage = self.config.get('usage', f'{self.prefix}{self.name}')
        usage = usage.replace('{pfx}', self.prefix)
        usage = usage.replace('{cmd}', self.name)
        return usage

    @property
    def desc(self):
        tmp = self.config.get('description', 'No description provided.')
        if self.owner:
            tmp += '\n(Bot Owner Only)'
        return tmp

    @property
    def alts(self):
        return self.config.get('alts', [])

    @property
    def requirements(self):
        requirements = ['send_messages', 'embed_links']
        return (requirements + self.config.get('requirements', []))

    @property
    def command(self):
        return self.load_path(os.path.join(self.path, self.name))

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
        self.log.warning('ACCESS DENIED | '
                         f'{perms.permission_string} | '
                         f'USR: {perms.user.name} [{perms.user.id}] | '
                         f'SRV: {perms.server.name} [{perms.server.id}]')

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

    def is_ready(self, message):
        return self.bot.ready

    def can_use(self, message):
        if not self.bot.cfg.dsc.bot and message.author.id != self.bot.user.id:
            self.log.warning(f'{message.author.name} tried using me.')
            return False

        return True

    async def off_cooldown(self, message):
        cd_identifier = f'{self.name}_{message.author.id}'

        if self.bot.cool_down.cmd.on_cooldown(cd_identifier):
            await self.respond_with_icon(message, '🕦')
            return False

        self.bot.cool_down.cmd.set_cooldown(cd_identifier)
        return True

    async def has_permissions(self, message):
        perms = GlobalCommandPermissions(self, message)

        if perms.permitted:
            return True

        self.log_unpermitted(perms)
        await self.respond_with_icon(message, '⛔')

        if perms.response:
            try:
                await message.channel.send(embed=perms.response)
            except discord.Forbidden:
                pass

        return False

    async def can_send_guild_message(self, message):
        guild_allowed = ServerCommandPermissions(self, message)

        if guild_allowed.permitted:
            return True

        self.log.warning('ACCESS DENIED: This module or command is not allowed in this location.')
        await self.respond_with_icon(message, '⛔')
        return False

    async def meets_requirements(self, message):
        requirements = CommandRequirements(self, message)

        if requirements.reqs_met:
            return True

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

        return False

    async def can_execute(self, message):
        tests = [
            self.is_ready, self.can_use, self.off_cooldown,
            self.has_permissions, self.can_send_guild_message, self.meets_requirements
        ]

        for test in tests:
            result = test(message)
            if inspect.isawaitable(result):
                result = await result
            if not result:
                return False

        return True

    async def execute(self, message, args):
        command_id = secrets.token_hex(4)

        if not await self.can_execute(message):
            return

        self.log_command_usage(message, command_id)

        if message.guild:
            delete_command_message = self.db.get_guild_settings(message.guild.id, 'DeleteCommands')
            if delete_command_message:
                try:
                    await message.delete()
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    pass

        try:
            await getattr(self.command, self.name)(self, message, args)
            await add_cmd_stat(self.db, self, message, args, command_id)
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
