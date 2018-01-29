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


async def blacklistmodule(cmd, message, args):
    if args:
        if len(args) >= 2:
            target_id = args[0]
            try:
                target_id = int(target_id)
                valid_id = True
            except ValueError:
                valid_id = False
            if valid_id:
                target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.get_all_members())
                if target:
                    lookup = ' '.join(args[1:])
                    module_exists = False
                    for command in cmd.bot.modules.commands:
                        if cmd.bot.modules.commands[command].category.lower() == lookup.lower():
                            module_exists = True
                            break
                    if module_exists:
                        black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers
                        black_user_file = await black_user_collection.find_one({'UserID': target.id})
                        if black_user_file:
                            if 'Modules' in black_user_file:
                                modules = black_user_file['Modules']
                            else:
                                modules = []
                            if lookup.lower() in modules:
                                modules.append(lookup.lower())
                                icon = '🔓'
                                result = f'removed from the `{lookup.lower()}` blacklist.'
                            else:
                                modules.remove(lookup.lower())
                                icon = '🔒'
                                result = f'added to the `{lookup.lower()}` blacklist.'
                            up_data = {'$set': {'UserID': target.id, 'Modules': modules}}
                            await black_user_collection.update_one({'UserID': target.id}, up_data)
                        else:
                            new_data = {'UserID': target.id, 'Modules': [lookup.lower()]}
                            await black_user_collection.insert_one(new_data)
                            icon = '🔒'
                            result = f'added to the `{lookup.lower()}` blacklist.'
                        title = f'{icon} {target.name}#{target.discriminator} has been {result}.'
                        response = discord.Embed(color=0xFFCC4D, title=title)
                    else:
                        response = discord.Embed(color=0x696969, title='🔍 Unrecognized module name.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 User with that ID not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid ID.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing was inputted.')
    await message.channel.send(embed=response)
