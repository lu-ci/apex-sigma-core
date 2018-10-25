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


async def blacklistserver(cmd: SigmaCommand, pld: CommandPayload):
    if args:
        target_id = None
        if args[0].isdigit():
            target_id = int(args[0])
        if target_id:
            target = cmd.bot.get_guild(target_id)
            if target:
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedServers
                black_user_file = await black_user_collection.find_one({'server_id': target.id})
                if black_user_file:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.delete_one({'server_id': target.id})
                    icon, result = '🔓', 'un-blacklisted'
                else:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.insert_one({'server_id': target.id})
                    icon, result = '🔒', 'blacklisted'
                response = discord.Embed(color=0xFFCC4D, title=f'{icon} {target.name} has been {result}.')
                await cmd.db.cache.del_cache(target.id)
                await cmd.db.cache.del_cache(f'{target.id}_checked')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing guild ID.')
    await message.channel.send(embed=response)
