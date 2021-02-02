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

import arrow
import discord

from sigma.core.utilities.generic_responses import denied, info
from sigma.modules.moderation.punishments.auto_punish.autopunishlevels import parse_time


async def mutedusers(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        now = arrow.utcnow().int_timestamp
        hm_lookup = {'server_id': pld.msg.guild.id, 'time': {'$gt': now}}
        hard_mute_list = await cmd.db[cmd.db.db_nam].HardmuteClockworkDocs.find(hm_lookup).to_list(None)
        text_mute_list = pld.settings.get('muted_users') or []
        if text_mute_list or hard_mute_list:
            response = discord.Embed(color=0x696969, title='🔇 Currently Muted Users')
            if text_mute_list:
                text_muted = []
                for user_id in text_mute_list:
                    user = pld.msg.guild.get_member(user_id)
                    info_txt = f'**{user.name}**#{user.discriminator}' if user else f'**{user_id}**'
                    user_lookup = {'server_id': pld.msg.guild.id, 'user_id': user_id, 'time': {'$gt': now}}
                    user_doc = await cmd.db[cmd.db.db_nam].TextmuteClockworkDocs.find_one(user_lookup)
                    if user_doc:
                        expiry = parse_time(user_doc.get('time') - now)
                        info_txt += f' (expires in {expiry})'
                    text_muted.append(info_txt)
                response.add_field(name='Text Muted', value='\n'.join(text_muted), inline=False)
            if hard_mute_list:
                hard_muted = []
                for user_doc in hard_mute_list:
                    user_id = user_doc.get('user_id')
                    user = pld.msg.guild.get_member(user_id)
                    info_txt = f'**{user.name}**#{user.discriminator}' if user else f'**{user_id}**'
                    if user_doc:
                        expiry = parse_time(user_doc.get('time') - now)
                        info_txt += f' (expires in {expiry})'
                    hard_muted.append(info_txt)
                response.add_field(name='Hard Muted', value='\n'.join(hard_muted), inline=False)
        else:
            response = info('No users are currently muted.')
    else:
        response = denied('Access Denied. Manage Messages needed.')
    await pld.msg.channel.send(embed=response)
