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

import secrets

import arrow
import discord

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.utilities.data_processing import get_broad_target, user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.punishments.auto_punish.auto_punish_mechanics import auto_punish

ACTION_MAP = {
    'textmute': ('🔇', 0x696969),
    'hardmute': ('🔇', 0x696969),
    'kick': ('👢', 0xc1694f),
    'softban': ('🔨', 0x993300),
    'ban': ('🔨', 0x993300)
}

PAST_MAP = {
    'textmute': 'text-muted',
    'hardmute': 'hard-muted',
    'kick': 'kicked',
    'softban': 'soft-banned',
    'ban': 'banned'
}


def warning_data(author, target, reason):
    """
    :type author: discord.Member
    :type target: discord.Member
    :type reason: str
    :rtype: dict
    """
    data = {
        'guild': author.guild.id,
        'moderator': {
            'id': author.id,
            'name': author.name,
            'discriminator': author.discriminator,
            'nickname': author.display_name
        },
        'target': {
            'id': target.id,
            'name': target.name,
            'discriminator': author.discriminator,
            'nickname': author.display_name
        },
        'warning': {
            'id': secrets.token_hex(2),
            'active': True,
            'reason': reason,
            'timestamp': arrow.utcnow().float_timestamp
        }
    }
    return data


def make_log_embed(author, target, warn_ident, reason):
    """
    :type author: discord.Member
    :type target: discord.Member
    :type warn_ident: str
    :type reason: str
    :rtype: discord.Embed
    """
    target_avatar = user_avatar(target)
    author_descrp = f'{author.mention}\n{author.name}#{author.discriminator}'
    target_descrp = f'{target.mention}\n{target.name}#{target.discriminator}'
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'{target.name} has been warned by {author.name}.', icon_url=target_avatar)
    response.add_field(name='⚠ Warned User', value=target_descrp)
    response.add_field(name='🛡 Moderator', value=author_descrp)
    if reason:
        response.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    response.set_footer(text=f'[{warn_ident}] User ID: {target.id}')
    return response


async def make_incident(db, gld, ath, trg, reason):
    """
    :type db: sigma.core.mechanics.database.Database
    :type gld: discord.Guild
    :type ath: discord.Member
    :type trg: discord.Member
    :type reason: str
    """
    icore = get_incident_core(db)
    inc = icore.generate('warn')
    inc.set_location(gld)
    inc.set_moderator(ath)
    inc.set_target(trg)
    inc.set_reason(reason)
    await icore.save(inc)
    await icore.report(gld, inc.to_embed('⚠', 0xFFCC4D))


async def check_auto_punish(cmd, pld, target):
    """
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member or discord.User
    """
    levels = pld.settings.get('auto_punish_levels') or {}
    if levels:
        lookup = {'guild': pld.msg.guild.id, 'target.id': target.id, 'warning.active': True}
        warnings = await cmd.db.col.Warnings.find(lookup).to_list(None)
        warning_count = str(len(warnings))
        level_data = levels.get(warning_count)
        if level_data:
            action = level_data.get('action')
            duration = level_data.get('duration')
            await auto_punish(cmd, pld, target, action, duration)
            icon, color = ACTION_MAP.get(action)
            title = f'{icon} {target.name} has been {PAST_MAP.get(action)}.'
            ap_embed = discord.Embed(color=color, title=title)
            lvl_word = 'warning' if warning_count == 1 else 'warnings'
            ap_embed.set_footer(text=f'Auto-Punished for accruing {warning_count} {lvl_word}.')
            await pld.msg.channel.send(embed=ap_embed)


async def issuewarning(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_messages:
        target = get_broad_target(pld)
        if target:
            if target.id != pld.msg.author.id:
                if not target.bot:
                    reason = ' '.join(pld.args[1:]) if pld.args[1:] else None
                    warn_data = warning_data(pld.msg.author, target, reason)
                    warn_ident = warn_data.get('warning').get('id')
                    await cmd.db.col.Warnings.insert_one(warn_data)
                    response = GenericResponse(f'Warning {warn_ident} issued to {target.name}.').ok()
                    await make_incident(cmd.db, pld.msg.guild, pld.msg.author, target, reason)
                    log_embed = make_log_embed(pld.msg.author, target, warn_ident, reason)
                    await log_event(cmd.bot, pld.settings, log_embed, 'log_warnings')
                    await check_auto_punish(cmd, pld, target)
                    guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon.url else None
                    to_target = discord.Embed(color=0xFFCC4D)
                    to_target.add_field(name='⚠ You received a warning.', value=f'Reason: {reason}')
                    to_target.set_footer(text=f'From {pld.msg.guild.name}', icon_url=guild_icon)
                    # noinspection PyBroadException
                    try:
                        await target.send(embed=to_target)
                    except Exception:
                        pass
                else:
                    response = GenericResponse('You can\'t warn bots.').error()
            else:
                response = GenericResponse('You can\'t warn yourself.').error()
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Messages needed.').denied()
    await pld.msg.channel.send(embed=response)
