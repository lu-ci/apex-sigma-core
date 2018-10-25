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
from sigma.core.utilities.generic_responses import permission_denied
from sigma.modules.moderation.permissions.permit import get_target_type, get_targets

filter_names = ['arguments', 'extensions', 'words', 'invites']


async def filterunignore(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 3:
                filter_name = args[1].lower()
                target_type = get_target_type(args[0].lower())
                if target_type:
                    if filter_name in filter_names:
                        targets, valid = get_targets(message, args, target_type)
                        if valid:
                            overrides = await cmd.db.get_guild_settings(message.guild.id, 'filter_overrides') or {}
                            override_data = overrides.get(filter_name)
                            if not override_data:
                                override_data = {'users': [], 'channels': [], 'roles': []}
                            override = override_data.get(target_type) or []
                            error_response = None
                            for target in targets:
                                if target.id in override:
                                    override.remove(target.id)
                                else:
                                    title = f'❗ {target.name} didn\'t have an override for that filter.'
                                    error_response = discord.Embed(color=0xBE1931, title=title)
                                    break
                            if not error_response:
                                override_data.update({target_type: override})
                                overrides.update({filter_name: override_data})
                                await cmd.db.set_guild_settings(message.guild.id, 'filter_overrides', overrides)
                                if len(targets) > 1:
                                    starter = f'{len(targets)} {target_type}'
                                    title = f'✅ {starter} are now affected by `blocked{filter_name}`.'
                                else:
                                    pnd = '#' if target_type == 'channels' else ''
                                    title = f'✅ {pnd}{targets[0].name} is now affected by `blocked{filter_name}`.'
                                response = discord.Embed(color=0x77B255, title=title)
                            else:
                                await message.channel.send(embed=error_response)
                                return
                        else:
                            if targets:
                                response = discord.Embed(color=0x696969, title=f'🔍 {targets} not found.')
                            else:
                                ender = 'specified' if target_type == 'roles' else 'targeted'
                                response = discord.Embed(color=0x696969, title=f'🔍 No {target_type} {ender}.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Invalid filter.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid target type.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
