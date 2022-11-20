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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.permissions.nodes.permission_data import generate_cmd_data, get_all_perms


def get_targets(message, args, target_type):
    """
    :type message: discord.Message
    :type args: list[str]
    :type target_type: str
    :rtype: list, bool
    """
    targets, valid = None, False
    if target_type == 'channels':
        if message.channel_mentions:
            targets = message.channel_mentions
            valid = True
    elif target_type == 'users':
        if message.mentions:
            targets = message.mentions
            valid = True
    elif target_type == 'roles':
        targets = []
        lookups = ' '.join(args[2:]).split('; ')
        for lookup in lookups:
            role_search = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.roles)
            if role_search:
                targets.append(role_search)
            else:
                return lookup, False
        valid = True
    return targets, valid


def get_target_type(target_type):
    """
    :type target_type: str
    :rtype: str
    """
    if target_type in ['channel', 'channels']:
        target_type = 'channels'
    elif target_type in ['user', 'users']:
        target_type = 'users'
    elif target_type in ['role', 'roles']:
        target_type = 'roles'
    else:
        target_type = None
    return target_type


async def permit(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if pld.args:
            if len(pld.args) >= 3:
                if ':' in pld.args[1]:
                    target_type = get_target_type(pld.args[0].lower())
                    if target_type:
                        perm_mode = pld.args[1].split(':')[0].lower()
                        node_name = pld.args[1].split(':')[1].lower()

                        modes = {
                            'c': ('command_exceptions', cmd.bot.modules.commands, True),
                            'm': ('module_exceptions', cmd.bot.modules.categories, False)
                        }

                        mode_vars = modes.get(perm_mode)
                        if mode_vars:
                            exc_group, check_group, check_alts = mode_vars
                            targets, valid_targets = get_targets(pld.msg, pld.args, target_type)
                            if valid_targets:
                                perms = await get_all_perms(cmd.db, pld.msg)
                                if check_alts:
                                    if node_name in cmd.bot.modules.alts:
                                        node_name = cmd.bot.modules.alts[node_name]
                                if node_name in check_group:
                                    node_exc = perms[exc_group]
                                    if node_name in perms[exc_group]:
                                        inner_exc = node_exc[node_name]
                                    else:
                                        inner_exc = generate_cmd_data(node_name)[node_name]
                                    exc_usrs = inner_exc[target_type]

                                    bad_item = None
                                    for target in targets:
                                        if target.id not in exc_usrs:
                                            exc_usrs.append(target.id)
                                            inner_exc.update({target_type: exc_usrs})
                                            node_exc.update({node_name: inner_exc})
                                            perms.update({exc_group: node_exc})
                                        else:
                                            bad_item = target
                                            break

                                    if not bad_item:
                                        await cmd.db.cache.del_cache(pld.msg.guild.id)
                                        await cmd.db[cmd.db.db_nam].Permissions.update_one(
                                            {'server_id': pld.msg.guild.id}, {'$set': perms}
                                        )

                                        if len(targets) > 1:
                                            title = f'{len(targets)} {target_type} can now use `{node_name}`.'
                                            response = GenericResponse(title).ok()
                                        else:
                                            pnd = '#' if target_type == 'channels' else ''
                                            title = f'{pnd}{targets[0].name} can now use `{node_name}`.'
                                            response = GenericResponse(title).ok()
                                    else:
                                        pnd = '#' if target_type == 'channels' else ''
                                        title = f'{pnd}{bad_item.name} already has an override for `{node_name}`.'
                                        response = GenericResponse(title).warn()
                                else:
                                    perm_type = 'Command' if perm_mode == 'c' else 'Module'
                                    response = GenericResponse(f'{perm_type} not found.').not_found()
                            else:
                                if targets:
                                    response = GenericResponse(f'{targets} not found.').not_found()
                                else:
                                    ender = 'specified' if target_type == 'roles' else 'targeted'
                                    response = GenericResponse(f'No {target_type} {ender}.').not_found()
                        else:
                            response = GenericResponse('Unrecognized lookup mode, see usage example.').error()
                    else:
                        response = GenericResponse('Invalid target type.').error()
                else:
                    response = GenericResponse('Separate permission type and name with a colon.').error()
            else:
                response = GenericResponse('Not enough arguments.').error()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
