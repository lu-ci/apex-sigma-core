# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

import asyncio

import discord


class GlobalCommandPermissions(object):
    def __init__(self, command, message):
        self.message = message
        self.bot = command.bot
        self.cmd = command
        self.db = command.db
        self.loop = asyncio.get_event_loop()
        # Default States
        self.nsfw_denied = False
        self.black_user = False
        self.black_srv = False
        self.owner_denied = False
        self.partner_denied = False
        self.module_denied = False
        self.dm_denied = False
        self.permitted = True
        self.response = None
        # Check Calls
        self.check_nsfw()
        self.check_dmable()
        self.check_owner()

    def check_dmable(self):
        if not self.message.guild:
            if self.cmd.dmable:
                self.dm_denied = False
            else:
                self.dm_denied = True
        else:
            self.dm_denied = False

    def check_nsfw(self):
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
        if 'Modules' in black_user_file:
            if self.cmd.category in black_user_file['Modules']:
                black_user = True
                self.module_denied = True
            else:
                black_user = False
        else:
            black_user = False
        return black_user

    async def check_black_usr(self):
        black_user_collection = self.db[self.bot.cfg.db.database].BlacklistedUsers
        black_user_file = await black_user_collection.find_one({'UserID': self.message.author.id})
        if black_user_file:
            if 'Total' in black_user_file:
                if black_user_file['Total']:
                    self.black_user = True
                else:
                    self.black_user = self.check_black_mdl(black_user_file)
            else:
                self.black_user = self.check_black_mdl(black_user_file)
        else:
            self.black_user = False

    async def check_black_srv(self):
        if self.message.guild:
            black_srv_collection = self.db[self.bot.cfg.db.database].BlacklistedServers
            black_srv_file = await black_srv_collection.find_one({'ServerID': self.message.guild.id})
            if black_srv_file:
                self.black_srv = True
            else:
                self.black_srv = False
        else:
            self.black_srv = False

    def check_owner(self):
        auth = self.message.author
        owners = self.bot.cfg.dsc.owners
        if self.cmd.owner:
            if auth.id in owners:
                self.owner_denied = False
            else:
                self.owner_denied = True
        else:
            self.owner_denied = False

    async def generate_response(self):
        prefix = await self.bot.get_prefix(self.message)
        if self.black_srv:
            return
        elif self.black_user:
            return
        elif self.dm_denied:
            color = 0xBE1931
            title = f'⛔ Can\'t Be Used In Direct Messages'
            desc = f'Please use {prefix}{self.cmd.name} on a server where I am present.'
        elif self.owner_denied:
            color = 0xBE1931
            title = '⛔ Bot Owner Only'
            desc = f'I\'m sorry {self.message.author.display_name}. I\'m afraid I can\'t let you do that.'
        elif self.nsfw_denied:
            if self.message.guild:
                color = 0x744EAA
                title = f'🍆 NSFW Commands Are Not Allowed In #{self.message.channel.name}'
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


class ServerCommandPermissions(object):
    def __init__(self, command, message):
        self.cmd = command
        self.db = self.cmd.db
        self.bot = self.cmd.bot
        self.msg = message
        self.permitted = True

    def check_mdl_overwrites(self, perms):
        mdl_overwritten = False
        mdl_exc = perms['ModuleExceptions']
        author = self.msg.author
        if mdl_exc:
            mdl_name = self.cmd.plugin_info['category']
            if mdl_name in mdl_exc:
                exceptions = mdl_exc[mdl_name]
                if author.id in exceptions['Users']:
                    mdl_overwritten = True
                if self.msg.channel.id in exceptions['Channels']:
                    mdl_overwritten = True
                for role in author.roles:
                    if role.id in exceptions['Roles']:
                        mdl_overwritten = True
                        break
        return mdl_overwritten

    def check_cmd_overwrites(self, perms):
        cmd_overwritten = False
        cmd_exc = perms['CommandExceptions']
        author = self.msg.author
        if cmd_exc:
            if self.cmd.name in cmd_exc:
                exceptions = cmd_exc[self.cmd.name]
                if author.id in exceptions['Users']:
                    cmd_overwritten = True
                if self.msg.channel.id in exceptions['Channels']:
                    cmd_overwritten = True
                for role in author.roles:
                    if role.id in exceptions['Roles']:
                        cmd_overwritten = True
                        break
        return cmd_overwritten

    @staticmethod
    def cross_permits(mdl_o, cmd_o, mdl_d, cmd_d):
        if mdl_d or cmd_d:
            if mdl_o:
                if cmd_d:
                    if cmd_o:
                        override = True
                    else:
                        override = False
                else:
                    override = True
            else:
                if cmd_o:
                    override = True
                else:
                    override = False
        else:
            override = True
        return override

    async def check_perms(self):
        if self.msg.guild:
            author = self.msg.author
            is_guild_admin = author.permissions_in(self.msg.channel).administrator
            if not is_guild_admin and author.id not in self.bot.cfg.dsc.owners:
                # Crunderwood was here...
                perms = await self.db[self.bot.cfg.db.database].Permissions.find_one({'ServerID': self.msg.guild.id})
                if not perms:
                    permitted = True
                else:
                    cmd = self.cmd.name
                    mdl = self.cmd.plugin_info['category']
                    mdl_override = self.check_mdl_overwrites(perms)
                    if mdl in perms['DisabledModules']:
                        mdl_disabled = True
                    else:
                        mdl_disabled = False
                    cmd_override = self.check_cmd_overwrites(perms)
                    if cmd in perms['DisabledCommands']:
                        cmd_disabled = True
                    else:
                        cmd_disabled = False
                    permitted = self.cross_permits(mdl_override, cmd_override, mdl_disabled, cmd_disabled)
            else:
                permitted = True
        else:
            permitted = True
        self.permitted = permitted
        return permitted
