# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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
from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate, get_image_colors
from sigma.modules.moderation.permissions.nodes.permission_data import get_all_perms


async def disabledmodules(cmd: SigmaCommand, message: discord.Message, args: list):
    page = args[0] if args else 1
    perms = await get_all_perms(cmd.db, message)
    disabled_modules = perms['DisabledModules']
    overridden_modules = perms['ModuleExceptions']
    disabled_list = []
    for dmdl_name in disabled_modules:
        if dmdl_name in cmd.bot.modules.categories:
            if dmdl_name in overridden_modules:
                dmdl_name += '\*'
            disabled_list.append(dmdl_name)
    if disabled_list:
        disabled_count = len(disabled_list)
        disabled_list, page_num = paginate(disabled_list, page, 50)
        title = f'{message.guild.name} Disabled Modules'
        info_text = f'[Page {page_num}] Showing {len(disabled_list)} out of {disabled_count} disabled modules.'
        response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
        response.set_author(name=title, icon_url=message.guild.icon_url)
        response.description = ', '.join(disabled_list)
        response.set_footer(text=info_text)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No disabled modules found.')
    await message.channel.send(embed=response)
