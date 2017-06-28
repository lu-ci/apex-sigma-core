import discord


class CommandPermissions(object):
    def __init__(self, command, message):
        self.message = message
        self.bot = command.bot
        self.cmd = command
        self.db = command.db
        # Check States
        self.nsfw_denied = False
        self.black_user = False
        self.black_serv = False
        self.owner_denied = False
        self.partner_denied = False
        self.dm_denied = False
        self.permitted = True
        self.response = None
        # Check Calls
        self.check_nsfw()
        self.check_dmable()
        self.check_final()
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
        if self.cmd.rating == 0:
            self.nsfw_denied = False
        else:
            nsfw_collection = self.db[self.bot.cfg.db.database].NSFWPermissions
            channel_nsfw_file = nsfw_collection.find_one({'channel_id': self.message.channel.id})
            if channel_nsfw_file:
                allowed_rating = channel_nsfw_file['rating']
                if self.cmd.rating > allowed_rating:
                    self.nsfw_denied = True
                else:
                    self.nsfw_denied = False
            else:
                self.nsfw_denied = True

    def generate_response(self):
        if self.dm_denied:
            color = 0xDB0000
            title = f'⛔ Can\'t Be Used In Direct Messages'
            desc = f'Please use {self.bot.cfg.pref.prefix}{self.cmd.name} on a server where I am present.'
        elif self.nsfw_denied:
            color = 0x9933FF
            title = f'🍆 NSFW Commands Are Not Allowed In #{self.message.channel.name}.'
            desc = f'If you are an administrator on {self.message.guild.name} '
            desc += f'Please use **`{self.bot.cfg.pref.prefix}nsfwpermit {self.cmd.rating}`** '
            desc += f'in #{self.message.channel.name} to permit commands that are rated '
            desc += f'{self.cmd.rating} and lower to be used there.'
        else:
            return
        response = discord.Embed(color=color)
        response.add_field(name=title, value=desc)
        self.response = response

    def check_final(self):
        checklist = [
            self.dm_denied,
            self.nsfw_denied,
            self.black_serv,
            self.black_user,
            self.owner_denied,
            self.partner_denied,
        ]
        for check in checklist:
            if check is True:
                self.permitted = False
                break
