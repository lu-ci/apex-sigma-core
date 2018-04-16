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


async def shadowpollpermit(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            poll_id = args[0].lower()
            if message.mentions:
                perm_type = 'users'
                target = message.mentions[0]
            elif message.channel_mentions:
                perm_type = 'channels'
                target = message.channel_mentions[0]
            else:
                lookup = ' '.join(args[1:]).lower()
                perm_type = 'roles'
                target = discord.utils.find(lambda x: x.name.lower() == lookup, message.guild.roles)
            if target:
                poll_file = await cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    author = poll_file['origin']['author']
                    if author == message.author.id:
                        if target.id not in poll_file['permissions'][perm_type]:
                            poll_file['permissions'][perm_type].append(target.id)
                            await cmd.db[cmd.db.db_cfg.database].ShadowPolls.update_one({'id': poll_id},
                                                                                        {'$set': poll_file})
                            response = discord.Embed(color=0x66CC66, title=f'✅ {target.name} has been permitted.')
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ {target.name} is already permitted.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Target not located.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID and target.')
    await message.channel.send(embed=response)
