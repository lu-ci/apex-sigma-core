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

import secrets

import arrow

scaler_cache = None


class CommandRateLimiter(object):
    """
    Miniature cooldown handler to rate-limit command spamming.
    """

    __slots__ = ("cmd", "stamps")

    def __init__(self, cmd):
        """
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        :param cmd: The command instance.
        """
        self.cmd = cmd
        self.stamps = {}

    def is_cooling(self, message):
        """
        Check if the command is on cooldown or not.
        :type message: discord.Message
        :param message: The message that triggered the command.
        :return:
        """
        timeout = self.cmd.bot.cool_down.get_scaled(message.author.id, 1.25)
        last_stamp = self.stamps.get(message.author.id, 0)
        curr_stamp = arrow.utcnow().float_timestamp
        return (last_stamp + timeout) > curr_stamp

    def set_cooling(self, message):
        """
        Set the command to be on cooldown.
        :type message: discord.Message
        :param message: The message that triggered the command.
        :return:
        """
        if message.author.id not in self.cmd.bot.cfg.dsc.owners:
            self.stamps.update({message.author.id: arrow.utcnow().float_timestamp})


class CooldownControl(object):
    """
    Cooldown core that checks, gets, sets and processes cooldowns.
    """

    def __init__(self, bot):
        """
        :type bot: sigma.core.sigma.ApexSigma
        :param bot: The main client core.
        """
        self.bot = bot
        self.db = self.bot.db
        self.cds = self.db[self.db.db_nam].CooldownSystem
        self.scaling = {}

    async def on_cooldown(self, cmd, user):
        """
        Checks if the function for the given user is still on cooldown or not.
        :type cmd: str
        :type user: discord.User or str
        :param cmd: The command or function the cooldown is bound to.
        :param user: The user that the cooldown is bound to.
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry.get('end_stamp', 0)
            now_stamp = arrow.utcnow().int_timestamp
            if now_stamp > end_stamp:
                cooldown = False
            else:
                cooldown = True
        else:
            cooldown = False
        return cooldown

    async def get_cooldown(self, cmd, user):
        """
        Gets the amount of time remaining for the cooldown to expire.
        :type cmd: str
        :type user: discord.User or str
        :param cmd: The command or function the cooldown is bound to.
        :param user: The user that the cooldown is bound to.
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry.get('end_stamp', 0)
            now_stamp = arrow.utcnow().float_timestamp
            cooldown = end_stamp - now_stamp
            if cooldown < 2:
                if cooldown <= 0:
                    cooldown = 0.01
                else:
                    cooldown = round(cooldown, 2)
            else:
                cooldown = int(cooldown)
        else:
            cooldown = 0
        return cooldown

    async def set_cooldown(self, cmd, user, amount):
        """
        :type cmd: str
        :type user: discord.User or str
        :type amount: int
        :param cmd: The command or function the cooldown is bound to.
        :param user: The user that the cooldown is bound to.
        :param amount: The cooldown time in seconds.
        :return:
        """
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            if user.id in self.bot.cfg.dsc.owners:
                amount = 0
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        end_stamp = arrow.utcnow().int_timestamp + amount
        if entry:
            await self.cds.update_one({'name': cd_name}, {'$set': {'end_stamp': end_stamp}})
        else:
            cd_data = {'name': cd_name, 'end_stamp': end_stamp}
            await self.cds.insert_one(cd_data)

    async def clean_cooldowns(self):
        """
        Purges all cooldown timers from the database that have already expired.
        :return:
        """
        now = arrow.utcnow().int_timestamp
        await self.cds.delete_many({'end_stamp': {'$lt': now}})

    def get_scaled(self, uid, base, multiplier=5):
        """
        Scales a cooldown amount based on incrementing usage.
        :type uid: int
        :type base: int or float
        :type multiplier: int or float
        :param uid: User ID of the invoking user.
        :param base: Base cooldown amount to scale.
        :param multiplier: Maximum capped cooldown multiplier.
        :return:
        """
        last_entry = self.scaling.get(uid, {})
        last_stamp = last_entry.get('stamp', 0)
        last_count = last_entry.get('count', 0)
        now_stamp = arrow.utcnow().int_timestamp
        if now_stamp - last_stamp > base * multiplier:
            cooldown = base
            data_entry = {'stamp': now_stamp, 'count': 0}
        else:
            mod_base, mod_divider = 1125, 1000
            modifier = (int(mod_base * 0.8) + secrets.randbelow(int(mod_base * 0.2))) / mod_divider
            cooldown = base * (1 + (modifier * last_count))
            data_entry = {'stamp': now_stamp, 'count': last_count + 1}
        self.scaling.update({uid: data_entry})
        return int(cooldown)
