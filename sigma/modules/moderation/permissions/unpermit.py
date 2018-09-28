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
from sigma.core.mechanics.permissions import scp_cache
from sigma.modules.moderation.permissions.nodes.permission_data import get_all_perms, generate_cmd_data


def get_perm_mode(cmd: SigmaCommand, args: list):
    perm_tuple, valid = None, True
    modes = {
        'c': ('command_exceptions', cmd.bot.modules.commands, True),
        'm': ('module_exceptions', cmd.bot.modules.categories, False)
    }
    if ':' in args[1]:
        perm_mode, cmd_name = args[1].split(':')
        cmd_name = cmd_name.lower()
        perm_mode = perm_mode.lower()
        if perm_mode == 'c':
            mode_vars = modes.get(perm_mode)
        elif perm_mode == 'm':
            mode_vars = modes.get(perm_mode)
        else:
            valid = False
            return perm_tuple, valid
        perm_tuple = (perm_mode, cmd_name) + mode_vars
    else:
        valid = False
    return perm_tuple, valid


async def get_perm_group(cmd: SigmaCommand, message: discord.Message, perm_tuple: tuple, perm_type: str):
    perm_mode, cmd_name, exception_group, check_group, check_alts = perm_tuple
    exception_tuple = None
    if check_alts:
        if cmd_name in cmd.bot.modules.alts:
            cmd_name = cmd.bot.modules.alts[cmd_name]
    if cmd_name in check_group:
        perms = await get_all_perms(cmd.db, message)
        cmd_exc = perms[exception_group]
        if cmd_name in perms[exception_group]:
            inner_exc = cmd_exc[cmd_name]
        else:
            inner_exc = generate_cmd_data(cmd_name)[cmd_name]
        exc_usrs = inner_exc[perm_type]
        exception_tuple = (exc_usrs, inner_exc, cmd_exc, perms)
    return exception_tuple


def get_targets(message: discord.Message, args: list, perm_type: str):
    targets, valid = None, False
    if perm_type == 'channels':
        if message.channel_mentions:
            targets = message.channel_mentions
            valid = True
    elif perm_type == 'users':
        if message.mentions:
            targets = message.mentions
            valid = True
    elif perm_type == 'roles':
        targets = []
        lookups = ' '.join(args[2:]).split('; ')
        for lookup in lookups:
            role_search = discord.utils.find(lambda x: x.name.lower() == lookup.strip(), message.guild.roles)
            if role_search:
                targets.append(role_search)
            else:
                targets, valid = lookup, False
                break
        valid = True
    return targets, valid


def verify_targets(targets: list, exception_tuple: tuple, cmd_name: str, exception_group: str, perm_type: str):
    exc_usrs, inner_exc, cmd_exc, perms = exception_tuple
    bad_item = False
    for target in targets:
        if target.id in exc_usrs:
            exc_usrs.remove(target.id)
            inner_exc.update({perm_type: exc_usrs})
            cmd_exc.update({cmd_name: inner_exc})
            perms.update({exception_group: cmd_exc})
        else:
            bad_item = target
            break
    return bad_item


def get_perm_type(perm_type: str):
    if perm_type in ['channel', 'channels']:
        perm_type = 'channels'
    elif perm_type in ['user', 'users']:
        perm_type = 'users'
    elif perm_type in ['role', 'roles']:
        perm_type = 'roles'
    else:
        perm_type = None
    return perm_type


async def unpermit(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 3:
                if ';' in args[1]:
                    perm_type = get_perm_type(args[0].lower())
                    if perm_type:
                        targets, valid_targets = get_targets(message, args, perm_type)
                        if valid_targets:
                            perm_tuple, valid_perms = get_perm_mode(cmd, args)
                            if valid_perms:
                                perm_mode, cmd_name, exception_group, check_group, check_alts = perm_tuple
                                exception_tuple = await get_perm_group(cmd, message, perm_tuple, perm_type)
                                if exception_tuple:
                                    exc_usrs, inner_exc, cmd_exc, perms = exception_tuple
                                    bad_item = verify_targets(targets, exception_tuple, cmd_name, exception_group, perm_type)
                                    if not bad_item:
                                        await cmd.db[cmd.db.db_nam].Permissions.update_one(
                                            {'server_id': message.guild.id}, {'$set': perms})
                                        scp_cache.del_cache(message.guild.id)
                                        if len(targets) > 1:
                                            title = f'✅ {len(targets)} {perm_type} can no longer use `{cmd_name}`.'
                                        else:
                                            pnd = '#' if perm_type == 'channels' else ''
                                            title = f'✅ {pnd}{targets[0].name} can no longer use `{cmd_name}`.'
                                        response = discord.Embed(color=0x77B255, title=title)
                                    else:
                                        pnd = '#' if perm_type == 'channels' else ''
                                        title = f'⚠ {pnd}{bad_item.name} didn\'t have an override for `{cmd_name}`.'
                                        response = discord.Embed(color=0xFFCC4D, title=title)
                                else:
                                    perm_type = 'Command' if perm_mode == 'c' else 'Module'
                                    response = discord.Embed(color=0x696969, title=f'🔍 {perm_type} not found.')
                            else:
                                response = discord.Embed(color=0xBE1931, title='❗ Invalid permission type.')
                        else:
                            if targets:
                                response = discord.Embed(color=0x696969, title=f'🔍 {targets} not found.')
                            else:
                                ender = 'specified' if perm_type == 'roles' else 'targeted'
                                response = discord.Embed(color=0x696969, title=f'🔍 No {perm_type} {ender}.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Invalid permission type.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Separate permission type and name with a colon.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
