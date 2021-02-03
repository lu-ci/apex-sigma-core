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


async def blacklistuser(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            target_id = abs(int(pld.args[0]))
        except ValueError:
            target_id = None
        if target_id:
            if target_id not in cmd.bot.cfg.dsc.owners:
                target = await cmd.bot.get_user(target_id)
                if target:
                    target_id = target.id
                    target_name = target.name
                else:
                    target_name = target_id
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers
                black_user_file = await black_user_collection.find_one({'user_id': target_id})
                if black_user_file:
                    if black_user_file.get('total'):
                        update_data = {'$set': {'user_id': target_id, 'total': False}}
                        icon, result = '🔓', 'un-blacklisted'
                    else:
                        update_data = {'$set': {'user_id': target_id, 'total': True}}
                        icon, result = '🔒', 'blacklisted'
                    await black_user_collection.update_one({'user_id': target_id}, update_data)
                else:
                    await black_user_collection.insert_one({'user_id': target_id, 'total': True})
                    icon, result = '🔒', 'blacklisted'
                await cmd.db.cache.del_cache(target_id)
                await cmd.db.cache.del_cache(f'{target_id}_checked')
                title = f'{icon} {target_name} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = GenericResponse('That target is immune.').error()
        else:
            response = GenericResponse('Invalid user ID.').error()
    else:
        response = GenericResponse('Missing user ID.').error()
    await pld.msg.channel.send(embed=response)
