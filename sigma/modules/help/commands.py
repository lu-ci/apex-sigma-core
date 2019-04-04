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

import discord

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.permissions import ServerCommandPermissions
from sigma.core.utilities.generic_responses import not_found


async def commands(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        lookup = pld.args[0].lower()
        command_items = cmd.bot.modules.commands
        command_list = []
        for command in command_items:
            command = command_items[command]
            category = command.category.lower()
            if category == lookup:
                if pld.msg.guild:
                    permission = ServerCommandPermissions(command, pld.msg)
                    await permission.check_perms()
                else:
                    permission = None
                command_list.append([command, permission])
        if command_list:
            module_list = sorted(command_list, key=lambda x: x[0].name)
            module_count = len(module_list)
            page = pld.args[1] if len(pld.args) > 1 else 1
            module_list, page = PaginatorCore.paginate(module_list, page, 30)
            output = ''
            for module_item, module_perm in module_list:
                if module_perm:
                    if module_perm.permitted:
                        output += f'\n- {module_item.name}'
                    else:
                        output += f'\n- ⛔ {module_item.name}'
                else:
                    output += f'\n- {module_item.name}'
                if module_item.alts:
                    output += f' [{", ".join(module_item.alts)}]'
            if output:
                title_text = f'```py\nThere are {module_count} commands.\n```'
                response = discord.Embed(color=0x1B6F5F)
                response.add_field(name=f'{lookup.upper()} Commands', value=title_text, inline=False)
                response.add_field(name=f'Commands List | Page {page}', value=f'```yml\n{output}\n```', inline=False)
            else:
                response = not_found(f'No commands on page {page}.')
        else:
            response = not_found('Module not found.')
    else:
        pfx = cmd.db.get_prefix(pld.settings)
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
        response.add_field(name='Modules', value=module_list_out, inline=False)
        response.add_field(name='Module List', value=f'```yml\n{output}\n```', inline=False)
        response.set_footer(text=f'Type {pfx}{cmd.name} [module] to see commands in that module.')
    await pld.msg.channel.send(embed=response)
