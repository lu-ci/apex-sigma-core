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


async def blacklistcommand(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if len(pld.args) >= 2:
            try:
                target_id = abs(int(pld.args[0]))
            except ValueError:
                target_id = None
            if target_id:
                target = await cmd.bot.get_user(target_id)
                if target:
                    target_id = target.id
                    target_name = target.name
                else:
                    target_name = target_id
                lookup = ' '.join(pld.args[1:])
                if lookup.lower() in cmd.bot.modules.alts:
                    lookup = cmd.bot.modules.alts[lookup.lower()]
                if lookup.lower() in cmd.bot.modules.commands:
                    black_file = await cmd.db.col.BlacklistedUsers.find_one({'user_id': target_id})
                    commands = black_file.get('commands', [])
                    if lookup.lower() in commands:
                        commands.remove(lookup.lower())
                        icon, result = '🔓', f'removed from the `{lookup.lower()}` blacklist'
                    else:
                        commands.append(lookup.lower())
                        icon, result = '🔒', f'added to the `{lookup.lower()}` blacklist'
                    title = f'{icon} {target_name} has been {result}.'
                    response = discord.Embed(color=0xFFCC4D, title=title)
                    update_data = {'$set': {'user_id': target_id, 'commands': commands}}
                    await cmd.db.col.BlacklistedUsers.update_one({'user_id': target_id}, update_data, upsert=True)
                    await cmd.db.cache.del_cache(target_id)
                    await cmd.db.cache.del_cache(f'{target_id}_checked')
                else:
                    response = GenericResponse('Command not found.').not_found()
            else:
                response = GenericResponse('Invalid user ID.').error()
        else:
            response = GenericResponse('Not enough arguments.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
