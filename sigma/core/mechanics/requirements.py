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


class CommandRequirements(object):
    """
    Handles the checking of a command's execution requirements.
    """

    __slots__ = ("cmd", "msg", "reqs", "chn", "reqs_met", "missing_list")

    def __init__(self, cmd, message):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        :type message: discord.Message
        """
        self.cmd = cmd
        self.msg = message
        self.reqs = cmd.requirements
        self.chn = self.msg.channel
        self.reqs_met = True
        self.missing_list = []
        self.check_requirements()

    def check_requirements(self):
        """
        Starts the checking of all requirements for the given command.
        """
        if self.msg.guild:
            for requirement in self.reqs:
                req_status = getattr(self.chn.permissions_for(self.msg.guild.me), requirement)
                if not req_status:
                    self.missing_list.append(requirement)
                    self.reqs_met = False
