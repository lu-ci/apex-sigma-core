import discord


async def commands(cmd, message, args):
    if args:
        lookup = ' '.join(args).lower()
        command_items = cmd.bot.modules.commands
        command_list = []
        for command in command_items:
            command = command_items[command]
            category = command.category.lower()
            if category == lookup:
                command_list.append(command)
        if command_list:
            module_list = sorted(command_list, key=lambda x: x.name)
            output = ''
            for module_item in module_list:
                output += f'\n- {module_item.name}'
                if module_item.alts:
                    output += f' [{", ".join(module_item.alts)}]'
            title_text = f'```py\nThere are {len(module_list)} commands.\n```'
            response = discord.Embed(color=0x1B6F5F)
            response.add_field(name=f'{lookup.upper()} Commands', value=title_text, inline=False)
            response.add_field(name='Commands List', value=f'```yml\n{output}\n```', inline=False)
        else:
            response = discord.Embed(color=0x696969, title='🔍 Nothing was found...')
    else:
        pfx = cmd.bot.get_prefix(message)
        response = discord.Embed(color=0xBE1931, title=f'❗ Please input a module from {pfx}modules.')
    await message.channel.send(embed=response)
