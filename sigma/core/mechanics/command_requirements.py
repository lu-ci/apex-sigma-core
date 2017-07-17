class CommandRequirements(object):
    def __init__(self, cmd, message):
        self.cmd = cmd
        self.msg = message
        self.reqs = cmd.requirements
        self.chn = self.msg.channel
        self.me = self.msg.guild.me
        self.reqs_met = True
        self.missing_list = []
        self.check_requirements()

    def check_requirements(self):
        if self.msg.guild:
            for requirement in self.reqs:
                req_status = getattr(self.me.permissions_in(self.chn), requirement)
                if not req_status:
                    self.missing_list.append(requirement)
                    self.reqs_met = False
