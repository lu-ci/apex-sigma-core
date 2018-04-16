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

from importlib import reload as reimport

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.development.command_md import command_md
from sigma.modules.development.version_updater import version_updater


async def reload(cmd: SigmaCommand, message: discord.Message, args: list):
    await version_updater(cmd)
    await command_md(cmd)
    if not args:
        cmd.log.info('---------------------------------')
        cmd.log.info('Reloading all modules...')
        cmd.bot.ready = False
        response = discord.Embed(color=0xF9F9F9, title='⚗ Reloading all modules...')
        load_status = await message.channel.send(embed=response)
        cmd.bot.init_modules()
        cmd_count = len(cmd.bot.modules.commands)
        ev_count = 0
        for key in cmd.bot.modules.events:
            event_group = cmd.bot.modules.events[key]
            ev_count += len(event_group)
        load_end_title = f'✅ Loaded {cmd_count} Commands and {ev_count} Events.'
        load_done_response = discord.Embed(color=0x77B255, title=load_end_title)
        await load_status.edit(embed=load_done_response)
        cmd.bot.ready = True
        cmd.log.info(f'Loaded {cmd_count} commands and {ev_count} events.')
        cmd.log.info('---------------------------------')
    else:
        command_name = ' '.join(args)
        if command_name in cmd.bot.modules.alts:
            command_name = cmd.bot.modules.alts[command_name]
        response = discord.Embed()
        if command_name not in cmd.bot.modules.commands.keys():
            response.colour = 0xBE1931
            response.title = f'❗ Command `{command_name}` was not found.'
        else:
            module_to_reload = cmd.bot.modules.commands[command_name].command
            reimport(module_to_reload)
            response.colour = 0x77B255
            response.title = f'✅ Command `{command_name}` was reloaded.'
        await message.channel.send(embed=response)
