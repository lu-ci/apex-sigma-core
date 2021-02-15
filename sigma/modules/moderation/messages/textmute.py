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

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.utilities.data_processing import convert_to_seconds, user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    """
    :type message: discord.Message
    :type target: discord.Member
    :type reason: str
    :rtype: discord.Embed
    """
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name='A Member Has Been Muted', icon_url=user_avatar(target))
    log_embed.add_field(name='🔇 Muted User',
                        value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_embed.add_field(name='🛡 Responsible',
                        value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_embed.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_embed.set_footer(text=f'User ID {target.id}')
    return log_embed


async def make_incident(db, gld, ath, trg, reason):
    """
    :type db: sigma.core.mechanics.database.Database
    :type gld: discord.Guild
    :type ath: discord.Member
    :type trg: discord.Member
    :type reason: str
    """
    icore = get_incident_core(db)
    inc = icore.generate('textmute')
    inc.set_location(gld)
    inc.set_moderator(ath)
    inc.set_target(trg)
    if reason:
        inc.set_reason(reason)
    await icore.save(inc)
    await icore.report(gld, inc.to_embed('🔇', 0x696969))


async def textmute(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        response = GenericResponse('Access Denied. Manage Messages needed.').denied()
    else:
        if not pld.msg.mentions:
            response = GenericResponse('No user targeted.').error()
        else:
            author = pld.msg.author
            target = pld.msg.mentions[0]
            if author.id == target.id:
                response = GenericResponse('Can\'t mute yourself.').error()
            elif cmd.bot.user.id == target.id:
                response = GenericResponse('I can\'t mute myself.').error()
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier:
                    response = GenericResponse('Can\'t mute someone equal or above you.').denied()
                else:
                    timed = pld.args[-1].startswith('--time=')
                    try:
                        now = arrow.utcnow().int_timestamp
                        endstamp = now + convert_to_seconds(pld.args[-1].split('=')[-1]) if timed else None
                    except (LookupError, ValueError):
                        err_response = GenericResponse('Please use the format HH:MM:SS.').error()
                        await pld.msg.channel.send(embed=err_response)
                        return
                    mute_list = pld.settings.get('muted_users')
                    if mute_list is None:
                        mute_list = []
                    if target.id in mute_list:
                        response = GenericResponse(f'{target.display_name} is already text-muted.').error()
                    else:
                        mute_list.append(target.id)
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'muted_users', mute_list)
                        response = GenericResponse(f'{target.display_name} has been text-muted.').ok()
                        rarg = pld.args[1:-1] if timed else pld.args[1:] if pld.args[1:] else None
                        reason = ' '.join(rarg) if rarg else None
                        await make_incident(cmd.db, pld.msg.guild, pld.msg.author, target, reason)
                        log_embed = generate_log_embed(pld.msg, target, reason)
                        await log_event(cmd.bot, pld.settings, log_embed, 'log_mutes')
                        guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
                        to_target_title = '🔇 You have been text-muted.'
                        to_target = discord.Embed(color=0x696969)
                        to_target.add_field(name=to_target_title, value=f'Reason: {reason}')
                        to_target.set_footer(text=f'On: {pld.msg.guild.name}', icon_url=guild_icon)
                        try:
                            await target.send(embed=to_target)
                        except (discord.Forbidden, discord.HTTPException):
                            pass
                        if endstamp:
                            doc_data = {'server_id': pld.msg.guild.id, 'user_id': target.id, 'time': endstamp}
                            await cmd.db[cmd.db.db_nam].TextmuteClockworkDocs.insert_one(doc_data)
    await pld.msg.channel.send(embed=response)
