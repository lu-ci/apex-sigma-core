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

import asyncio

import discord


class GlobalCommandPermissions(object):
    """
    Handles the main core permissions of commands
    such as if the command is DM-able, owner only, nsfw,
    if a user or guild has been blacklisted from using it,
    and similar limitations.
    """

    __slots__ = (
        "pld", "message", "settings", "cmd", "bot",
        "db", "loop", "nsfw_denied", "black_user", "black_srv",
        "owner_denied", "partner_denied", "module_denied",
        "command_denied", "dm_denied", "permitted", "response"
    )

    def __init__(self, command, pld):
        """
        :param command: The command instance.
        :type command: sigma.core.mechanics.command.SigmaCommand
        :param pld: The message payload data.
        :type pld: sigma.core.mechanics.payload.CommandPayload
        """
        self.pld = pld
        self.message = self.pld.msg
        self.settings = self.pld.settings
        self.cmd = command
        self.bot = self.cmd.bot
        self.db = self.cmd.db
        self.loop = asyncio.get_event_loop()
        # Default States
        self.nsfw_denied = False
        self.black_user = False
        self.black_srv = False
        self.owner_denied = False
        self.partner_denied = False
        self.module_denied = False
        self.command_denied = False
        self.dm_denied = False
        self.permitted = True
        self.response = None
        # Check Calls
        self.check_nsfw()
        self.check_dmable()
        self.check_owner()

    def check_dmable(self):
        """
        Checks of the command can be used in direct messages.
        :return:
        :rtype:
        """
        if not self.message.guild:
            if self.cmd.dmable:
                self.dm_denied = False
            else:
                self.dm_denied = True
        else:
            self.dm_denied = False

    def check_nsfw(self):
        """
        Checks if the command is NSFW
        and if the place it's called is marked as NSFW.
        :return:
        :rtype:
        """
        if isinstance(self.message.channel, discord.TextChannel):
            if self.cmd.nsfw:
                if self.message.channel.is_nsfw():
                    self.nsfw_denied = False
                else:
                    self.nsfw_denied = True
            else:
                self.nsfw_denied = False
        else:
            self.nsfw_denied = False

    def check_black_mdl(self, black_user_file):
        """
        Checks if a user has been blacklisted
        from using the given module specifically.
        :param black_user_file: Users' blacklist data.
        :type black_user_file: dict
        :return:
        :rtype: bool
        """
        black_modules = black_user_file.get('modules', {})
        if self.cmd.category in black_modules:
            black_user = True
            self.module_denied = True
        else:
            black_user = False
        return black_user

    def check_black_cmd(self, black_user_file):
        """
        Checks if a user has been blacklisted
        from using the given command specifically.
        :param black_user_file: Users' blacklist data.
        :type black_user_file: dict
        :return:
        :rtype: bool
        """
        black_commands = black_user_file.get('commands', {})
        if self.cmd.name in black_commands:
            black_user = True
            self.command_denied = True
        else:
            black_user = False
        return black_user

    async def check_black_usr(self):
        """
        Checks if a user has been blacklisted from using
        the given command, either fully, module or command.
        :return:
        :rtype:
        """
        black_user_collection = self.db[self.bot.cfg.db.database].BlacklistedUsers
        black_user_file = await black_user_collection.find_one({'user_id': self.message.author.id})
        if black_user_file:
            if black_user_file.get('total'):
                self.black_user = True
            else:
                black_mdl = self.check_black_mdl(black_user_file)
                black_cmd = self.check_black_cmd(black_user_file)
                self.black_user = black_mdl or black_cmd
        else:
            self.black_user = False

    async def check_black_srv(self):
        """
        Checks if a guild has been blacklisted
        from using the given command.
        :return:
        :rtype:
        """
        if self.message.guild:
            black_srv_collection = self.db[self.bot.cfg.db.database].BlacklistedServers
            black_srv_file = await black_srv_collection.find_one({'server_id': self.message.guild.id})
            if black_srv_file:
                self.black_srv = True
            else:
                self.black_srv = False
        else:
            self.black_srv = False

    def check_owner(self):
        """
        Checks if the command is owner-only
        and if the user calling it is an owner.
        :return:
        :rtype:
        """
        auth = self.message.author
        owners = self.bot.cfg.dsc.owners
        if self.cmd.owner:
            if auth.id in owners:
                self.owner_denied = False
            else:
                self.owner_denied = True
        else:
            self.owner_denied = False

    def generate_response(self):
        """
        Generates embed reponses for some more
        common permission denials.
        :return:
        :rtype: discord.Embed
        """
        prefix = self.db.get_prefix(self.settings)
        if self.black_srv:
            return
        elif self.black_user:
            return
        elif self.dm_denied:
            color = 0xBE1931
            title = '⛔ Can\'t be used in direct messages.'
            desc = f'Please use {prefix}{self.cmd.name} on a server where I am present.'
        elif self.owner_denied:
            color = 0xBE1931
            title = '⛔ Developer Only'
            desc = f'I\'m sorry {self.message.author.display_name}. I\'m afraid I can\'t let you do that.'
        elif self.nsfw_denied:
            if self.message.guild:
                color = 0x744EAA
                title = f'🍆 NSFW Commands Are Not Allowed In #{self.message.channel.name}.'
                desc = 'Make sure the NSFW marker is enabled in the channel settings.'
            else:
                return
        elif self.partner_denied:
            color = 0x3B88C3
            title = '💎 Partner Servers Only'
            desc = 'Some commands are limited to only be usable by partners.'
            desc += '\nYou can request to be a partner server by visiting our '
            desc += 'server and telling us why you should be one.'
            desc += '\nYou can also become a partner by supporting us via our '
            desc += '[`Patreon`](https://www.patreon.com/ApexSigma) page.'
        else:
            return
        response = discord.Embed(color=color)
        response.add_field(name=title, value=desc)
        self.response = response

    def check_final(self):
        """
        Runs the final check which is
        going through all individual checks.
        If any has been triggered, the execution is intercepted.
        :return:
        :rtype:
        """
        checklist = [
            self.dm_denied,
            self.nsfw_denied,
            self.black_srv,
            self.black_user,
            self.owner_denied,
            self.partner_denied,
        ]
        for check in checklist:
            if check is True:
                self.permitted = False
                break

    def log_unpermitted(self):
        """
        ### Flags:
            - `u`: User Blacklisted
            - `s`: Server Blacklisted
            - `o`: Owner Only
            - `m`: Module Blacklisted
            - `c`: Command Blacklisted
            - `d`: Direct Message Not Allowed
            - `n`: NSFW Channels Only
            - `v`: Parter Only
        ### Example:
            `u---dn-` *User blacklisted, use in DM and use of NSFW command when not in NSFW channel.*
        """

        conds = [
            self.black_user,
            self.black_srv,
            self.owner_denied,
            self.module_denied,
            self.command_denied,
            self.dm_denied,
            self.nsfw_denied,
            self.partner_denied
        ]
        letters = ['u', 's', 'o', 'm', 'c', 'd', 'n', 'v']
        fmt = ''.join(map(lambda c, l: l if c else '-', conds, letters))
        log_line = (
            'ACCESS DENIED'
            f' | {fmt}'
            f' | USR: {self.message.author} ({self.message.author.id})'
        )
        if self.message.guild:
            log_line += f' | SRV: {self.message.guild} ({self.message.guild.id})'
        self.cmd.log.warning(log_line)


class ServerCommandPermissions(object):
    """
    Wraps and handles processing of server-specific permission settings.
    """

    __slots__ = ("cmd", "db", "bot", "msg", "permitted", "perm_coll")

    def __init__(self, command, message):
        """
        :param command: The command or event instance.
        :type command: sigma.core.mechanics.command.SigmaCommand or sigma.core.mechanics.event.SigmaEvent
        :param message: The message that triggered the command.
        :type message: discord.Message
        """
        self.cmd = command
        self.db = self.cmd.db
        self.bot = self.cmd.bot
        self.msg = message
        self.permitted = True
        self.perm_coll = self.db[self.bot.cfg.db.database].Permissions

    def check_mdl_overwrites(self, perms):
        """
        Checks if a module has overrides when it's disabled.
        :param perms: The guild's permission document.
        :type perms: dict
        :return:
        :rtype: bool
        """
        mdl_overwritten = False
        mdl_exc = perms.get('module_exceptions', {})
        author = self.msg.author
        if mdl_exc:
            mdl_name = self.cmd.module_info.get('category', 'unknown')
            if mdl_name in mdl_exc:
                exceptions = mdl_exc[mdl_name]
                if author.id in exceptions.get('users', []):
                    mdl_overwritten = True
                if self.msg.channel.id in exceptions.get('channels', []):
                    mdl_overwritten = True
                for role in author.roles:
                    if role.id in exceptions.get('roles', []):
                        mdl_overwritten = True
                        break
        return mdl_overwritten

    def check_cmd_overwrites(self, perms):
        """
        Checks if a command has overrides when it's disabled.
        :param perms: The guild's permission document.
        :type perms: dict
        :return:
        :rtype: bool
        """
        cmd_overwritten = False
        cmd_exc = perms.get('command_exceptions', {})
        author = self.msg.author
        if cmd_exc:
            if self.cmd.name in cmd_exc:
                exceptions = cmd_exc.get(self.cmd.name, {})
                if author.id in exceptions.get('users', []):
                    cmd_overwritten = True
                if self.msg.channel.id in exceptions.get('channels', []):
                    cmd_overwritten = True
                for role in author.roles:
                    if role.id in exceptions.get('roles', []):
                        cmd_overwritten = True
                        break
        return cmd_overwritten

    @staticmethod
    def cross_permits(mdl_o, cmd_o, mdl_d, cmd_d):
        """
        Cross-references permission of both modules and commands
        to determine if the function should be executed or not.
        :param mdl_o: Is the module overridden.
        :type mdl_o: bool
        :param cmd_o: Is the command overridden.
        :type cmd_o: bool
        :param mdl_d: Is the module disabled.
        :type mdl_d: bool
        :param cmd_d: Is the command disabled.
        :type cmd_d: bool
        :return:
        :rtype: bool
        """
        if mdl_d or cmd_d:
            if mdl_o:
                if cmd_d:
                    override = cmd_o
                else:
                    override = True
            else:
                override = cmd_o
        else:
            override = True
        return override

    async def check_perms(self):
        """
        The main permission checking method that calls the others.
        :return:
        :rtype: bool
        """
        if self.msg.guild:
            author = self.msg.author
            is_guild_admin = author.permissions_in(self.msg.channel).administrator
            if not is_guild_admin and author.id not in self.bot.cfg.dsc.owners:
                # Crunderwood was here...
                perms = await self.perm_coll.find_one({'server_id': self.msg.guild.id})
                if not perms:
                    permitted = True
                else:
                    cmd = self.cmd.name
                    mdl = self.cmd.module_info.get('category', 'unknown')
                    mdl_override = self.check_mdl_overwrites(perms)
                    disabled_modules = perms.get('disabled_modules', [])
                    mdl_disabled = mdl in disabled_modules
                    cmd_override = self.check_cmd_overwrites(perms)
                    disabled_commands = perms.get('disabled_commands', [])
                    cmd_disabled = cmd in disabled_commands
                    permitted = self.cross_permits(mdl_override, cmd_override, mdl_disabled, cmd_disabled)
            else:
                permitted = True
        else:
            permitted = True
        self.permitted = permitted
        return permitted


def check_filter_perms(msg, settings, filter_name):
    """
    Checks permissions for filtering functions.
    This is to avoid filtering administrators and overridden rules.
    :param msg: The message to process.
    :type msg: discord.Message
    :param settings: The guild's settings document,
    :type settings: dict
    :param filter_name: The name of the filter to check.
    :type filter_name: str
    :return:
    :rtype: bool
    """
    permitted = False
    overrides = settings.get('filter_overrides')
    if overrides:
        override = overrides.get(filter_name)
        if override:
            channels = override.get('channels', [])
            roles = override.get('roles', [])
            users = override.get('users', [])
            if msg.author.id in users:
                permitted = True
            if msg.channel:
                if msg.channel.id in channels:
                    permitted = True
            user_roles = [r.id for r in msg.author.roles]
            for role in roles:
                if role in user_roles:
                    permitted = True
                    break
    return permitted
