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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok


async def shadowpollunpermit(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        if len(pld.args) >= 2:
            poll_id = pld.args[0].lower()
            if pld.msg.mentions:
                perm_type = 'users'
                target = pld.msg.mentions[0]
                if not isinstance(target, discord.Member):
                    target = None
            elif pld.msg.channel_mentions:
                perm_type = 'channels'
                target = pld.msg.channel_mentions[0]
            else:
                lookup = ' '.join(pld.args[1:]).lower()
                perm_type = 'roles'
                target = discord.utils.find(lambda x: x.name.lower() == lookup, pld.msg.guild.roles)
            if target:
                poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    author = poll_file['origin']['author']
                    if author == pld.msg.author.id:
                        if target.id in poll_file['permissions'][perm_type]:
                            poll_file['permissions'][perm_type].remove(target.id)
                            await cmd.db[cmd.db.db_nam].ShadowPolls.update_one({'id': poll_id},
                                                                               {'$set': poll_file})
                            response = ok(f'{target.name} has been unpermitted.')
                        else:
                            response = error(f'{target.name} is not permitted.')
                    else:
                        response = denied('You didn\'t make this poll.')
                else:
                    response = not_found('Poll not found.')
            else:
                response = error('Target not located.')
        else:
            response = error('Not enough arguments.')
    else:
        response = error('Missing poll ID and target.')
    await pld.msg.channel.send(embed=response)
