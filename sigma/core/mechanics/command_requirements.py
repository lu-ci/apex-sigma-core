"""
Command Requirements:
    Ran on each message with a command.
    Makes the requirement class for a command.
    Used for checking if the bot has the needed permissions.
"""


class CommandRequirements(object):
    def __init__(self, cmd, message):
        self.cmd = cmd
        self.msg = message
        self.reqs = cmd.requirements
        self.chn = self.msg.channel
        self.reqs_met = True
        self.missing_list = []
        self.check_requirements()

    def check_requirements(self):
        """
        Runs the requirement check on creation.
        :return:
        """
        if self.msg.guild:
            for requirement in self.reqs:
                req_status = getattr(self.msg.guild.me.permissions_in(self.chn), requirement)
                if not req_status:
                    self.missing_list.append(requirement)
                    self.reqs_met = False
