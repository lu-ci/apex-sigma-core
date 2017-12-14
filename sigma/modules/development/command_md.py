import os


async def command_md(ev):
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
            output += f'\n- [{key.upper()}](#{key.lower()})'
        for key in key_list:
            output += '\n'
            output += f'\n### {key.upper()}'
            output += f'\nCommands | Description | Example'
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
