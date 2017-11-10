from sigma.core.mechanics.module_component import SigmaModuleComponent
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.event import SigmaEvent

class SigmaModule(SigmaModuleComponent):
    def __init__(self, manager, config):
        super().__init__(manager, config)

        self.manager = manager
        self.commands = {}
        self.events = {}
        self._alts = {}

        if self.manager.init:
            self.log.info(f'Loading the {self.name} Module')

        self.load_commands(config.get('commands', []))
        self.load_events(config.get('events', []))

    @property
    def alts(self):
        if self._alts:
            return self._alts

        for cmd_name, cmd in self.commands.items():
            for alt in cmd.alts:
                self._alts[alt] = cmd_name

        return self._alts

    def load_command(self, command_config):
        if self.bot.cfg.pref.music_only and self.category != 'music':
            return
        elif self.bot.cfg.pref.text_only and self.category == 'music':
            return

        cmd_name, cmd = SigmaCommand.from_config(self, command_config)
        self.commands[cmd_name] = cmd

        return (cmd_name, cmd)

    def load_commands(self, commands_config):
        if self.manager.init and commands_config:
            self.log.info('Loading Commands')

        for command_config in commands_config:
            self.load_command(command_config)

    def load_event(self, event_config):
        "Load a :single: event and add it to the events list"

        event_name, event = SigmaEvent.from_config(self, event_config)
        event_list = self.events.get(event.type, [])
        event_list.append(event)
        self.events[event.type] = event_list

        return (event_name, event)

    def load_events(self, events_config):
        "Load :all: events."

        if self.bot.cfg.dsc.bot and not self.bot.cfg.pref.music_only:
            if self.manager.init and events_config:
                self.log.info('Loading Events')

            for event_config in events_config:
                self.load_event(event_config)
