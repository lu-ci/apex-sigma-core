import discord


async def modules(cmd, message, args):
    commands = cmd.bot.modules.commands
    module_list = []
    for command in commands:
        command = commands[command]
        category = command.category.upper()
        if category not in module_list:
            module_list.append(category)
    module_list = sorted(module_list)
    output = ''
    for module_item in module_list:
        output += f'\n- {module_item}'
    response = discord.Embed(color=0x1B6F5F)
    response.add_field(name='Sigma Modules', value=f'```py\nThere are {len(module_list)} modules.\n```', inline=False)
    response.add_field(name='Module List', value=f'```yml\n{output}\n```', inline=False)
    await message.channel.send(embed=response)
