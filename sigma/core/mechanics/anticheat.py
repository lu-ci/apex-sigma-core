# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand


class AntiCheat(object):
    def __init__(self, bot):
        """
        The Anti-Cheat core class.
        To detect all them pesky botters.
        TODO: Pattern detection.
        DONE: Interval detection.
        DONE: Burst interval detection.
        DONE: Expectancy detection.
        DONE: Report channel relay.
        :param bot:
        """
        self.bot = bot
        self.data = {}
        self.expects = {}
        self.notified = {}

    def should_notify(self, uid: int):
        now = arrow.utcnow().float_timestamp
        stamp = self.notified.get(uid) or 0
        if now >= stamp + 300:
            notify = True
            self.notified.update({uid: now})
        else:
            notify = False
        return notify

    def get_data(self, uid: int):
        """
        Gets data from the command data storage cache.
        Kept in-memory, cause I'm sure the database wouldn't like this.
        The get method also cuts the entries to have only the latest 100.
        :param uid:
        :return:
        """
        data = self.data.get(uid) or []
        if len(data) > 100:
            cut_data = len(data) - 100
            data = data[cut_data:]
            self.data.update({uid: data})
        return data

    @staticmethod
    def create_data(cmd: SigmaCommand, msg: discord.Message):
        return {
            'cmd': cmd.name,
            'stamp': arrow.utcnow().float_timestamp,
            'created': arrow.get(msg.created_at).float_timestamp
        }

    def add_data(self, cmd: SigmaCommand, msg: discord.Message):
        """
        Adds a new data entry to the command cache.
        :param cmd:
        :param msg:
        :return:
        """
        uid = msg.author.id
        data = self.get_data(uid)
        addition = self.create_data(cmd, msg)
        data.append(addition)
        self.data.update({uid: data})

    def check_burst(self, uid: int):
        """
        Iterates through all cached command data for the given user.
        The iteration scans 5 entry chunks and looks for bursts in them.
        If 3 or more occurances are found where command got executed with
        less than an 0.8s interval between them, a "ding" is added.
        If there are 3 or more dings in all the entries, the function's
        suspiciousness is "True".
        :param uid:
        :return:
        """
        data = self.get_data(uid)
        done = False
        dings = 0
        counter = 0
        strangle = 0.8
        if len(data) >= 5:
            while not done:
                bursts = 0
                last_ex_stamp = 0
                last_cr_stamp = 0
                span = data[counter:counter + 5]
                for entry in span:
                    stamp = entry.get('stamp')
                    created = entry.get('created')
                    ex_diff = stamp - last_ex_stamp
                    cr_diff = created - last_cr_stamp
                    if ex_diff <= strangle or cr_diff <= strangle:
                        bursts += 1
                    last_ex_stamp = entry.get('stamp')
                    last_cr_stamp = entry.get('created')
                if bursts >= 3:
                    dings += 1
                if span[-1] == data[-1]:
                    done = True
                counter += 1
        if dings >= 3:
            suspicious = True
            message = f'Found {dings} burst dings in the last {len(data)} entries.'
        else:
            suspicious = False
            message = None
        return suspicious, message

    def add_expectancy(self, uid: int, data: dict):
        expects = self.expects.get(uid) or []
        expects.append(data)
        self.expects.update({uid: expects})

    def check_interval(self, uid: int):
        """
        Goes through all the cached data, splits the entries into sub-lists per command.
        Then compares the command execution interval for matches.
        Depending on the amount of matching invervals it will be either ignored,
        an expectance will be made, or if an overwhelming amount matches, it will be
        marked as a suspicious execution.
        :param uid:
        :return:
        """
        dings = 0
        cmd_groups = {}
        data = self.get_data(uid)
        expects = []
        dingers = []
        strangle = 0.75
        for entry in data:
            cmd = entry.get('cmd')
            cmd_entries = cmd_groups.get(cmd) or []
            cmd_entries.append(entry)
            cmd_groups.update({cmd: cmd_entries})
        for cg_key in cmd_groups.keys():
            last_ex_stamp = 0
            last_cr_stamp = 0
            last_ex_difference = 0
            last_cr_difference = 0
            cg_entries = cmd_groups.get(cg_key)
            for cmd_entry in cg_entries:
                if last_ex_stamp and last_cr_stamp:
                    ex_stamp = cmd_entry.get('stamp')
                    cr_stamp = cmd_entry.get('created')
                    ex_diff = ex_stamp - last_ex_stamp
                    cr_diff = cr_stamp - last_cr_stamp
                    if last_ex_difference and last_cr_difference:
                        ex_ding = last_ex_difference - strangle <= ex_diff <= last_ex_difference + strangle
                        cr_ding = last_cr_difference - strangle <= cr_diff <= last_cr_difference + strangle
                        if ex_ding or cr_ding:
                            dings += 1
                            if cg_key not in dingers:
                                dingers.append(cg_key)
                    last_ex_difference = ex_diff
                    last_cr_difference = cr_diff
                last_ex_stamp = cmd_entry.get('stamp')
                last_cr_stamp = cmd_entry.get('created')
                if cmd_entry == cg_entries[-1]:
                    if 6 > dings >= 3:
                        expect_data = {
                            'cmd': cmd_entry.get('cmd'),
                            'stamp': last_ex_stamp + last_ex_difference,
                            'created': last_cr_stamp + last_cr_difference
                        }
                        self.add_expectancy(uid, expect_data)
                        if cg_key not in expects:
                            expects.append(cg_key)
        if dings >= 6:
            suspicious = True
            message = f'Found {dings} dings in the last {len(data)} entries.'
            if dingers:
                message += f'\nDings triggered by {", ".join(dingers)}.'
            if expects:
                message += f'\nExpects triggered by {", ".join(expects)}.'
        else:
            suspicious = False
            message = None
        return suspicious, message

    def check_expectancy(self, cmd: SigmaCommand, msg: discord.Message):
        """
        Iterates through expected triggers if there are any.
        Checks for matching data, if data matches, mark it suspicious.
        :param msg:
        :param cmd:
        :return:
        """
        uid = msg.author.id
        expects = self.expects.get(uid) or []
        data = self.create_data(cmd, msg)
        strangle = 0.75
        ding = False
        ecmd_dinged = None
        to_be_removed = []
        if expects:
            ecmds = [ex for ex in expects if ex.get('cmd') == cmd.name]
            if ecmds:
                for ecmd in ecmds:
                    ecmd_ex_stamp = ecmd.get('stamp')
                    ecmd_cr_stamp = ecmd.get('created')
                    data_ex_stamp = data.get('stamp')
                    data_cr_stamp = data.get('created')
                    ex_ding = data_ex_stamp - strangle < ecmd_ex_stamp < data_ex_stamp + strangle
                    cr_ding = data_cr_stamp - strangle < ecmd_cr_stamp < data_cr_stamp + strangle
                    if ex_ding or cr_ding:
                        ding = True
                        cmdn = ecmd.get('cmd')
                        ecmd_dinged = f'Expected {cmdn} to get executed, and it did.'
                        break
        for tbr in to_be_removed:
            expects.remove(tbr)
        self.expects.update({uid: expects})
        return ding, ecmd_dinged

    def check_pattern(self, uid: int):
        """
        Grab a pattern for the given command.
        It's checked by checking the commands nearest neighbours.
        This has a high tolerance rate of 10 dings to be considered suspicious
        due to users being able to spam one command over a large time frame.
        :param uid:
        :return:
        """
        data = self.get_data(uid)
        loop_index = 0
        patterns = {}
        dings = 0
        patterned = []
        for entry in data:
            if len(data) - 1 > loop_index > 0:
                pattern = patterns.get(entry.get('cmd'))
                if pattern:
                    curr_pattern = [
                        data[loop_index - 1].get('cmd'),
                        entry.get('cmd'),
                        data[loop_index + 1].get('cmd')
                    ]
                    if curr_pattern == pattern:
                        patterned.append(entry.get('cmd'))
                        dings += 1
                    pattern = curr_pattern
                patterns.update({entry.get('cmd'): pattern})
            loop_index += 1
        if dings >= 12:
            suspicious = True
            message = f'Patterns for {", ".join(patterned)} spotted with {dings} dings.'
        else:
            suspicious = False
            message = None
        return suspicious, message

    def check(self, cmd: SigmaCommand, msg: discord.Message):
        """
        Runs all the checks for the given user.
        The checks are in the order of pattern, expectancy, burst, inverval.
        If a suspiciousness marker is triggered, a message is relayed to the
        main server's guard channel with a guard string indicating what has been triggered.
        :return:
        """
        uid = msg.author.id
        checks = {
            'p': self.check_pattern(uid),
            'e': self.check_expectancy(cmd, msg),
            'b': self.check_burst(uid),
            'i': self.check_interval(uid)
        }
        check_values = []
        check_messages = []
        outstring_chars = []
        for check in checks.keys():
            check_res, check_msg = checks.get(check)
            check_char = check if check_res else '-'
            outstring_chars.append(check_char)
            check_values.append(check_res)
            if check_msg:
                check_messages.append(check_msg)
        outstring = ''.join(outstring_chars).upper()
        reasons = '\n'.join(check_messages)
        if check_values[0]:
            suspicious = any(check_values[1:])
        else:
            suspicious = any(check_values)
        return suspicious, outstring, reasons
