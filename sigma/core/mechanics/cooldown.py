import arrow


class CommandCooldown(object):
    def __init__(self):
        """
        A class used for a command-specific cooldown.
        Meant to be used for rate limiting command spam.
        A user is able to use a specific command only once per 1.35s.
        """
        self.cooldowns = {}
        self.interval = 1.35

    def get_cooldown(self, ident):
        """
        Gets the cooldown for the user with the stated identifier.
        Meaning discord user id/snowflake.
        :param ident:
        :return:
        """
        cd_data = self.cooldowns.get(ident) or 0
        now = arrow.utcnow().float_timestamp
        cd = cd_data - now
        return cd

    def set_cooldown(self, ident):
        """
        Updates the cooldowns dict with the new value for the
        user with the given cooldown identifier.
        :param ident:
        :return:
        """
        now = arrow.utcnow().float_timestamp
        new_stamp = now + self.interval
        self.cooldowns.update({ident: new_stamp})

    def on_cooldown(self, ident):
        """
        A quick check to see if a command is one cooldown
        for the given user's identifier.
        :param ident:
        :return:
        """
        cd_data = self.cooldowns.get(ident) or 0
        now = arrow.utcnow().float_timestamp
        if cd_data > now:
            on_cd = True
        else:
            on_cd = False
        return on_cd


class CooldownControl(object):
    def __init__(self, bot):
        """
        The cooldown control core.
        A collection of functions to read cooldown data from mongo.
        Cooldowns are stored as MongoDB files so they persist.
        :param bot:
        """
        self.bot = bot
        self.cmd = CommandCooldown()
        self.db = self.bot.db
        self.cds = self.db[self.bot.cfg.db.database].CooldownSystem

    def on_cooldown(self, cmd, user):
        """
        A quick check to see if a user is on cool-down for the stated command.
        The user argument can be a simple string to be a generalized id.
        :param cmd:
        :param user:
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry['end_stamp']
            now_stamp = arrow.utcnow().timestamp
            if now_stamp > end_stamp:
                cooldown = False
            else:
                cooldown = True
        else:
            cooldown = False
        return cooldown

    def get_cooldown(self, cmd, user):
        """
        Returns the current cooldown in seconds for the given user and command.
        :param cmd:
        :param user:
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry['end_stamp']
            now_stamp = arrow.utcnow().float_timestamp
            cooldown = end_stamp - now_stamp
            if cooldown < 2:
                cooldown = round(cooldown, 2)
            else:
                cooldown = int(cooldown)
        else:
            cooldown = 0
        return cooldown

    def set_cooldown(self, cmd, user, amount):
        """
        Sets or updates the cooldown file for the user and command.
        The file is stored in MongoDB to persist after reboots.
        :param cmd:
        :param user:
        :param amount:
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
        end_stamp = arrow.utcnow().timestamp + amount
        if entry:
            self.cds.update_one({'name': cd_name}, {'$set': {'end_stamp': end_stamp}})
        else:
            cd_data = {
                'name': cd_name,
                'end_stamp': end_stamp
            }
            self.cds.insert_one(cd_data)
