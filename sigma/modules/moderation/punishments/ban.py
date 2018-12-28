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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar, convert_to_seconds
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import permission_denied
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name=f'A User Has Been Banned', icon_url=user_avatar(target))
    log_response.add_field(name='🔨 Banned User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_response.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_response.set_footer(text=f'User ID {target.id}')
    return log_response


async def ban(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).ban_members:
        if pld.msg.mentions:
            target = pld.msg.mentions[0]
            timed = pld.args[-1].startswith('--time=')
            try:
                now = arrow.utcnow().timestamp
                endstamp = now + convert_to_seconds(pld.args[-1].split('=')[-1]) if timed else None
            except (LookupError, ValueError):
                err_response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
                await pld.msg.channel.send(embed=err_response)
                return
            if len(pld.args) >= 2:
                try:
                    if endstamp:
                        clean_days = int(pld.args[-2])
                    else:
                        clean_days = int(pld.args[-1])
                except ValueError:
                    clean_days = 0
            else:
                clean_days = 0
            clean_days = clean_days if clean_days in [0, 1, 7] else 0
            if cmd.bot.user.id != target.id:
                if pld.msg.author.id != target.id:
                    above_hier = hierarchy_permit(pld.msg.author, target)
                    is_admin = pld.msg.author.permissions_in(pld.msg.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(pld.msg.guild.me, target)
                        if above_me:
                            rarg = pld.args[1:-1] if timed else pld.args[1:] if pld.args[1:] else None
                            reason = ' '.join(rarg) if rarg else None
                            response = discord.Embed(color=0x696969, title=f'🔨 The user has been banned.')
                            response_title = f'{target.name}#{target.discriminator}'
                            response.set_author(name=response_title, icon_url=user_avatar(target))
                            to_target = discord.Embed(color=0x696969)
                            to_target.add_field(name='🔨 You have been banned.', value=f'Reason: {reason}')
                            to_target.set_footer(text=f'From: {pld.msg.guild.name}.', icon_url=pld.msg.guild.icon_url)
                            try:
                                await target.send(embed=to_target)
                            except discord.Forbidden:
                                pass
                            audit_reason = f'By {pld.msg.author.name}#{pld.msg.author.discriminator}: {reason}'
                            await target.ban(reason=audit_reason, delete_message_days=clean_days)
                            log_embed = generate_log_embed(pld.msg, target, reason)
                            await log_event(cmd.bot, pld.settings, log_embed, 'log_bans')
                            if endstamp:
                                doc_data = {'server_id': pld.msg.guild.id, 'user_id': target.id, 'time': endstamp}
                                await cmd.db[cmd.db.db_nam].BanClockworkDocs.insert_one(doc_data)
                        else:
                            response = discord.Embed(color=0xBE1931, title='⛔ Target is above my highest role.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ Can\'t ban someone equal or above you.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You can\'t ban yourself.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t ban myself.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = permission_denied('Ban permissions')
    await pld.msg.channel.send(embed=response)
