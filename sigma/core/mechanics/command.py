import os
import yaml
import discord
import secrets
from sigma.core.mechanics.logger import create_logger
from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.mechanics.permissions import ServerCommandPermissions


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
        self.rating = 0
        self.owner = False
        self.partner = False
        self.dmable = False
        self.requirements = None
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
            self.requirements = self.command_info['requirements']
        if 'permissions' in self.command_info:
            permissions = self.command_info['permissions']
            if 'rating' in permissions:
                self.rating = permissions['rating']
            if 'owner' in permissions:
                self.owner = permissions['owner']
            if 'partner' in permissions:
                self.partner = permissions['partner']
            if 'dmable' in permissions:
                self.dmable = permissions['dmable']
        if self.owner:
            self.desc += '\n(Bot Owner Only)'

    def load_command_config(self):
        config_path = f'config/plugins/{self.name}'
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
        if args:
            arguments = ' '.join(args)
        else:
            arguments = None
        author_full = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
        log_text = f'USR: {author_full} | {cmd_location} | ARGS: {arguments}'
        self.log.info(log_text)

    def log_unpermitted(self, perms):
        log_text = f'ACCESS DENIED | '
        log_text += f'BUSR: {perms.black_user} | BSRV: {perms.black_srv} | OWNR: {perms.owner_denied} | '
        log_text += f'DM: {perms.dm_denied} | NSFW: {perms.nsfw_denied} | VIP: {perms.partner_denied}'
        self.log.warning(log_text)

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
            'TrackeBack': f'{exception.with_traceback}',
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
        if self.bot.ready:
            if message.guild:
                delete_command_message = self.db.get_guild_settings(message.guild.id, 'DeleteCommands')
                if delete_command_message:
                    try:
                        await message.delete()
                    except:
                        pass
            perms = GlobalCommandPermissions(self, message)
            guild_allowed = ServerCommandPermissions(self, message)
            if perms.permitted:
                if guild_allowed:
                    try:
                        self.log_command_usage(message, args)
                        await getattr(self.command, self.name)(self, message, args)
                    except self.get_exception() as e:
                        err_token = secrets.token_hex(16)
                        self.log_error(message, args, e, err_token)
                        title = '❗ An Error Occurred!'
                        err_text = 'Something seems to have gone wrong.'
                        err_text += '\nPlease send this token to our support server.'
                        err_text += f'\nThe invite link is in the **{self.bot.get_prefix(message)}help** command.'
                        err_text += f'\nToken: **{err_token}**'
                        error_embed = discord.Embed(color=0xDB0000)
                        error_embed.add_field(name=title, value=err_text)
                        try:
                            await message.author.send(embed=error_embed)
                        except Exception:
                            pass
                else:
                    self.log.warning('ACCESS DENIED: This module or command is not allowed on this server.')
            else:
                self.log_unpermitted(perms)
                if perms.response:
                    try:
                        await message.author.send(embed=perms.response)
                    except discord.Forbidden:
                        pass
