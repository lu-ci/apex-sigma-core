import discord


class GlobalCommandPermissions(object):
    def __init__(self, command, message):
        self.message = message
        self.bot = command.bot
        self.cmd = command
        self.db = command.db
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
        self.check_black_srv()
        self.check_black_usr()
        self.check_owner()
        self.check_final()
        # Get Response
        self.generate_response()

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

    def check_black_usr(self):
        black_user_collection = self.db[self.bot.cfg.db.database].BlacklistedUsers
        black_user_file = black_user_collection.find_one({'UserID': self.message.author.id})
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

    def check_black_srv(self):
        if self.message.guild:
            black_srv_collection = self.db[self.bot.cfg.db.database].BlacklistedServers
            black_srv_file = black_srv_collection.find_one({'ServerID': self.message.guild.id})
            if black_srv_file:
                self.black_srv = True
            else:
                self.black_srv = False
        else:
            self.black_srv = False

    def check_owner(self):
        auth = self.message.author
        ownrs = self.bot.cfg.dsc.owners
        if self.cmd.owner:
            if auth.id in ownrs:
                self.owner_denied = False
            else:
                self.owner_denied = True
        else:
            self.owner_denied = False

    def generate_response(self):
        if self.black_srv:
            return
        elif self.black_user:
            return
        elif self.dm_denied:
            color = 0xBE1931
            title = f'⛔ Can\'t Be Used In Direct Messages'
            desc = f'Please use {self.bot.get_prefix(self.message)}{self.cmd.name} on a server where I am present.'
        elif self.owner_denied:
            color = 0xBE1931
            title = '⛔ Bot Owner Only'
            desc = f'I\'m sorry {self.message.author.display_name}. I\'m afraid I can\'t let you do that.'
            desc += f'Unless you are in the `{self.bot.get_prefix(self.message)}owners` list, you can not use that.'
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
        self.permitted = self.check_perms()

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
    def cross_permits(mdl_o, cmd_o):
        if mdl_o and cmd_o:
            override = True
        elif mdl_o and not cmd_o:
            override = False
        elif not mdl_o and cmd_o:
            override = True
        else:
            override = False
        return override

    def check_perms(self):
        if self.msg.guild:
            author = self.msg.author
            is_guild_admin = author.permissions_in(self.msg.channel).administrator
            if not is_guild_admin and author.id not in self.bot.cfg.dsc.owners:
                # Crunderwood was here...
                perms = self.db[self.bot.cfg.db.database].Permissions.find_one({'ServerID': self.msg.guild.id})
                if not perms:
                    permitted = True
                else:
                    cmd = self.cmd.name
                    mdl = self.cmd.plugin_info['category']
                    if mdl in perms['DisabledModules']:
                        if self.check_mdl_overwrites(perms):
                            mdl_override = True
                        else:
                            mdl_override = False
                    else:
                        if self.check_mdl_overwrites(perms):
                            mdl_override = True
                        else:
                            mdl_override = False
                    if cmd in perms['DisabledCommands']:
                        if self.check_cmd_overwrites(perms):
                            cmd_override = True
                        else:
                            cmd_override = False
                    else:
                        if self.check_cmd_overwrites(perms):
                            cmd_override = True
                        else:
                            cmd_override = False
                    permitted = self.cross_permits(mdl_override, cmd_override)
            else:
                permitted = True
        else:
            permitted = True
        return permitted
