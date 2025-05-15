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
import io

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def blacklistmembers(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    attachment = None
    if pld.args:
        try:
            target_id = abs(int(pld.args[0]))
        except ValueError:
            target_id = None
        if target_id:
            target_srv = await cmd.bot.get_guild(target_id)
            if not target_srv:
                try:
                    target_srv = await cmd.bot.fetch_guild(target_id)
                except discord.HTTPException:
                    target_srv = None
            if target_srv:
                target_id = target_srv.id
                target_name = target_srv.name
                srv_black_file = await cmd.db.col.BlacklistedServers.find_one({'server_id': target_id})
                if not srv_black_file:
                    await cmd.db.col.BlacklistedServers.insert_one({'server_id': target_id})
                await cmd.db.cache.del_cache(target_id)
                await cmd.db.cache.del_cache(f'{target_id}_checked')
                target_members = [member async for member in target_srv.fetch_members(limit=None)]
                total_member_count = len(target_members)
                banned_member_count = 0
                already_banned_count = 0
                report_lines = []
                for member in target_members:
                    action = 'skipped'
                    if not member.bot:
                        if member.id not in cmd.bot.cfg.dsc.owners:
                            usr_black_file = await cmd.db.col.BlacklistedUsers.find_one({'user_id': member.id}) or {}
                            if not usr_black_file.get('total'):
                                update_data = {'$set': {'user_id': member.id, 'total': True}}
                                await cmd.db.col.BlacklistedUsers.update_one(
                                    {'user_id': member.id},
                                    update_data,
                                    upsert=True
                                )
                                await cmd.db.cache.del_cache(member.id)
                                await cmd.db.cache.del_cache(f'{member.id}_checked')
                                banned_member_count += 1
                                action = 'blacklisted'
                            else:
                                already_banned_count += 1
                    report_entry = [
                        action,
                        str(member.id),
                        member.name,
                        'bot' if member.bot else 'normal'
                    ]
                    report_lines.append(report_entry)
                report_body = '\n'.join(['\t'.join(report_entry) for report_entry in report_lines])
                buffer = io.StringIO(report_body)
                attachment = discord.File(fp=buffer, filename=f'blacklisted_report_{target_id}.tsv')
                response = discord.Embed(color=0xFFCC4D, title=f'🔒 {target_name}\'s members have been blacklisted.')
                response.description = (
                    f'Total: {total_member_count}; '
                    f'New: {banned_member_count}; '
                    f'Old: {already_banned_count}.'
                )
            else:
                response = GenericResponse('Guild not present on this shard, if at all.').not_found()
        else:
            response = GenericResponse('Invalid guild ID.').error()
    else:
        response = GenericResponse('Missing guild ID.').error()
    await pld.msg.channel.send(embed=response, file=attachment)
