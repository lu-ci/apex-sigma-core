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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok
from sigma.modules.moderation.permissions.permit import get_target_type, get_targets

filter_names = ['arguments', 'extensions', 'words', 'invites']


async def filterunignore(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            if len(pld.args) >= 3:
                filter_name = pld.args[1].lower()
                target_type = get_target_type(pld.args[0].lower())
                if target_type:
                    if filter_name in filter_names:
                        targets, valid = get_targets(pld.msg, pld.args, target_type)
                        if valid:
                            overrides = pld.settings.get('filter_overrides') or {}
                            override_data = overrides.get(filter_name)
                            if not override_data:
                                override_data = {'users': [], 'channels': [], 'roles': []}
                            override = override_data.get(target_type) or []
                            error_response = None
                            for target in targets:
                                if target.id in override:
                                    override.remove(target.id)
                                else:
                                    error_response = error(f'{target.name} didn\'t have an override for that filter.')
                                    break
                            if not error_response:
                                override_data.update({target_type: override})
                                overrides.update({filter_name: override_data})
                                await cmd.db.set_guild_settings(pld.msg.guild.id, 'filter_overrides', overrides)
                                if len(targets) > 1:
                                    starter = f'{len(targets)} {target_type}'
                                    response = ok(f'{starter} are now affected by `blocked{filter_name}`.')
                                else:
                                    pnd = '#' if target_type == 'channels' else ''
                                    response = ok(f'{pnd}{targets[0].name} is now affected by `blocked{filter_name}`.')
                            else:
                                await pld.msg.channel.send(embed=error_response)
                                return
                        else:
                            if targets:
                                response = not_found(f'{targets} not found.')
                            else:
                                ender = 'specified' if target_type == 'roles' else 'targeted'
                                response = not_found(f'No {target_type} {ender}.')
                    else:
                        response = error('Invalid filter.')
                else:
                    response = error('Invalid target type.')
            else:
                response = error('Not enough arguments.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
