# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
  # Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
        pfx = await cmd.bot.get_prefix(message)
        command_list = cmd.bot.modules.commands
        module_list = []
        for command in command_list:
            command = command_list[command]
            category = command.category.upper()
            if category not in module_list:
                module_list.append(category)
        module_list = sorted(module_list)
        output = ''
        for module_item in module_list:
            output += f'\n- {module_item}'
        module_list_out = f'```py\nThere are {len(module_list)} modules.\n```'
        response = discord.Embed(color=0x1B6F5F)
        response.add_field(name='Sigma Modules', value=module_list_out, inline=False)
        response.add_field(name='Module List', value=f'```yml\n{output}\n```', inline=False)
        response.set_footer(text=f'Type {pfx}{cmd.name} [module] to see commands in that module.')
    await message.channel.send(embed=response)
