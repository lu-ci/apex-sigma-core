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

import os


async def command_md(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    if ev.bot.cfg.pref.dev_mode:
        if not os.path.exists('docs/information'):
            os.makedirs('docs/information')
        categories = {}
        for cmd_nam in ev.bot.modules.commands:
            cat = ev.bot.modules.commands[cmd_nam].category
            if cat in categories:
                cmd_list = categories[cat]
            else:
                cmd_list = []
            cmd_list.append(ev.bot.modules.commands[cmd_nam])
            categories.update({cat: cmd_list})
        key_list = sorted(list(categories))
        prefix = '>>'
        patreon_url = 'https://www.patreon.com/ApexSigma'
        output = f'**Hey there!** We need your **help**! Come support us on [**Patreon**]({patreon_url})!'
        output += '\n'
        output += '\n## Module Index'
        for key in key_list:
            output += f'\n- [{key.upper().replace("_", " ")}](#{key.lower().replace("_", "-")})'
        for key in key_list:
            output += '\n'
            output += f'\n### {key.upper().replace("_", " ")}'
            output += '\nCommands | Description | Example'
            output += '\n----------|-------------|--------'
            commands_in_cat = categories[key]
            sorted_commands = sorted(commands_in_cat, key=lambda x: x.name)
            for command in sorted_commands:
                command_names = f'`{prefix}{command.name}`'
                if command.alts:
                    for alt in command.alts:
                        command_names += f' `{prefix}{alt}`'
                usage = command.usage.replace('{cmd}', command.name).replace('{pfx}', '')
                command_desc = command.desc.replace('\n', ' ')
                command_usage = f'{prefix}{usage}'
                output += f'\n{command_names} | {command_desc} | `{command_usage}`'
            output += '\n[Back To Top](#module-index)'
        with open('docs/information/commands.md', 'w', encoding='utf-8') as commands_md_file:
            commands_md_file.write(output)
        ev.log.info('Updated Command List.')
