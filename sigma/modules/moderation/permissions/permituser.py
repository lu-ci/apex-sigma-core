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

from .nodes.permission_data import get_all_perms, generate_cmd_data


async def permituser(cmd, message, args):
    if args:
        if len(args) >= 2:
            if not message.author.permissions_in(message.channel).manage_guild:
                response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
            else:
                if message.mentions:
                    target = message.mentions[0]
                    error_response = discord.Embed(color=0xBE1931, title='❗ Bad Input')
                    try:
                        perm_mode, cmd_name = args[0].split(':')
                    except ValueError:
                        await message.channel.send(embed=error_response)
                        return
                    cmd_name = cmd_name.lower()
                    perm_mode = perm_mode.lower()
                    if perm_mode == 'c':
                        exception_group = 'CommandExceptions'
                        check_group = cmd.bot.modules.commands
                        check_alts = True
                    elif perm_mode == 'm':
                        exception_group = 'ModuleExceptions'
                        check_group = cmd.bot.modules.categories
                        check_alts = False
                    else:
                        await message.channel.send(embed=error_response)
                        return
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
                        exc_usrs = inner_exc['Users']
                        if target.id in exc_usrs:
                            response = discord.Embed(color=0xFFCC4D,
                                                     title=f'⚠ {target.name} can already use `{cmd_name}`')
                        else:
                            exc_usrs.append(target.id)
                            inner_exc.update({'Users': exc_usrs})
                            cmd_exc.update({cmd_name: inner_exc})
                            perms.update({exception_group: cmd_exc})
                            await cmd.db[cmd.db.db_cfg.database].Permissions.update_one({'ServerID': message.guild.id},
                                                                                        {'$set': perms})
                            response = discord.Embed(color=0x77B255,
                                                     title=f'✅ `{target.name}` can now use `{cmd_name}`.')
                    else:
                        response = discord.Embed(color=0x696969, title='🔍 Command/Module Not Found')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 No User Targeted')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not Enough Arguments')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Not Arguments Given')
    await message.channel.send(embed=response)
