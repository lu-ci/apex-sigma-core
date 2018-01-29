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


async def blacklistserver(cmd, message, args):
    if args:
        target_id = ''.join(args)
        try:
            target_id = int(target_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.guilds)
            if target:
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedServers
                black_user_file = await black_user_collection.find_one({'ServerID': target.id})
                if black_user_file:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.delete_one({'ServerID': target.id})
                    result = 'removed from the blacklist'
                    icon = '🔓'
                else:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.insert_one({'ServerID': target.id})
                    result = 'blacklisted'
                    icon = '🔒'
                title = f'{icon} {target.name} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)
