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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.permissions.permit import get_target_type, get_targets

filter_names = ['arguments', 'extensions', 'words', 'invites']


async def filterunignore(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
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
                                    error_response = GenericResponse(
                                        f'{target.name} didn\'t have an override for that filter.'
                                    ).error()
                                    break
                            if not error_response:
                                override_data.update({target_type: override})
                                overrides.update({filter_name: override_data})
                                await cmd.db.set_guild_settings(pld.msg.guild.id, 'filter_overrides', overrides)
                                if len(targets) > 1:
                                    starter = f'{len(targets)} {target_type}'
                                    response = GenericResponse(
                                        f'{starter} are now affected by `blocked{filter_name}`.'
                                    ).ok()
                                else:
                                    pnd = '#' if target_type == 'channels' else ''
                                    response = GenericResponse(
                                        f'{pnd}{targets[0].name} is now affected by `blocked{filter_name}`.'
                                    ).ok()
                            else:
                                await pld.msg.channel.send(embed=error_response)
                                return
                        else:
                            if targets:
                                response = GenericResponse(f'{targets} not found.').not_found()
                            else:
                                ender = 'specified' if target_type == 'roles' else 'targeted'
                                response = GenericResponse(f'No {target_type} {ender}.').not_found()
                    else:
                        response = GenericResponse('Invalid filter.').error()
                else:
                    response = GenericResponse('Invalid target type.').error()
            else:
                response = GenericResponse('Not enough arguments.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
