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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import denied, error, ok


def warning_data(author: discord.Member, target: discord.Member, reason: str):
    """

    :param author:
    :type author:
    :param target:
    :type target:
    :param reason:
    :type reason:
    :return:
    :rtype:
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


def make_log_embed(author: discord.Member, target: discord.Member, warn_iden, reason):
    """

    :param author:
    :type author:
    :param target:
    :type target:
    :param warn_iden:
    :type warn_iden:
    :param reason:
    :type reason:
    :return:
    :rtype:
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
    response.set_footer(text=f'[{warn_iden}] User ID: {target.id}')
    return response


async def make_incident(db: Database, gld: discord.Guild, ath: discord.Member, trg: discord.Member, reason: str):
    """

    :param db:
    :type db:
    :param gld:
    :type gld:
    :param ath:
    :type ath:
    :param trg:
    :type trg:
    :param reason:
    :type reason:
    """
    icore = get_incident_core(db)
    inc = icore.generate('warn')
    inc.set_location(gld)
    inc.set_moderator(ath)
    inc.set_target(trg)
    inc.set_reason(reason)
    await icore.save(inc)
    await icore.report(gld, inc.to_embed('⚠', 0xFFCC4D))


async def issuewarning(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_messages:
        if pld.msg.mentions:
            target = pld.msg.mentions[0]
            if target.id != pld.msg.author.id:
                if not target.bot:
                    reason = ' '.join(pld.args[1:]) if pld.args[1:] else None
                    warn_data = warning_data(pld.msg.author, target, reason)
                    warn_iden = warn_data.get('warning').get('id')
                    await cmd.db[cmd.db.db_nam].Warnings.insert_one(warn_data)
                    response = ok(f'Warning {warn_iden} issued to {target.name}.')
                    await make_incident(cmd.db, pld.msg.guild, pld.msg.author, target, reason)
                    log_embed = make_log_embed(pld.msg.author, target, warn_iden, reason)
                    await log_event(cmd.bot, pld.settings, log_embed, 'log_warnings')
                    to_target = discord.Embed(color=0xFFCC4D)
                    to_target.add_field(name='⚠ You received a warning.', value=f'Reason: {reason}')
                    to_target.set_footer(text=f'From {pld.msg.guild.name}', icon_url=pld.msg.guild.icon_url)
                    # noinspection PyBroadException
                    try:
                        await target.send(embed=to_target)
                    except Exception:
                        pass
                else:
                    response = error('You can\'t warn bots.')
            else:
                response = error('You can\'t warn yourself.')
        else:
            response = error('No user targeted.')
    else:
        response = denied('Access Denied. Manage Messages needed.')
    await pld.msg.channel.send(embed=response)
