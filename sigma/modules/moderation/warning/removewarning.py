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
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import GenericResponse


def make_log_embed(author, target, warn_ident):
    """
    :type author: discord.Member
    :type target: discord.Member
    :type warn_ident: str
    :rtype: discord.Embed
    """
    target_avatar = user_avatar(target)
    author_descrp = f'{author.mention}\n{author.name}#{author.discriminator}'
    target_descrp = f'{target.mention}\n{target.name}#{target.discriminator}'
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'{target.name} has been un-warned by {author.name}.', icon_url=target_avatar)
    response.add_field(name='⚠ Warned User', value=target_descrp)
    response.add_field(name='🛡 Moderator', value=author_descrp)
    response.set_footer(text=f'[{warn_ident}] User ID {target.id}')
    return response


async def make_incident(db, gld, ath, trg):
    """
    :type db: sigma.core.mechanics.database.Database
    :type gld: discord.Guild
    :type ath: discord.Member
    :type trg: discord.Member
    """
    icore = get_incident_core(db)
    inc = icore.generate('unwarn')
    inc.set_location(gld)
    inc.set_moderator(ath)
    inc.set_target(trg)
    await icore.save(inc)
    await icore.report(gld, inc.to_embed('⚠', 0xFFCC4D))


async def removewarning(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_messages:
        if pld.msg.mentions:
            if len(pld.args) == 2:
                target = pld.msg.mentions[0]
                warn_id = pld.args[1].lower()
                lookup = {
                    'guild': pld.msg.guild.id,
                    'target.id': target.id,
                    'warning.id': warn_id,
                    'warning.active': True
                }
                warn_data = await cmd.db.col.Warnings.find_one(lookup)
                if warn_data:
                    await make_incident(cmd.db, pld.msg.guild, pld.msg.author, target)
                    warn_ident = warn_data.get('warning').get('id')
                    change_data = {'$set': {'warning.active': False}}
                    await cmd.db.col.Warnings.update_one(lookup, change_data)
                    response = GenericResponse(f'Warning {warn_ident} deactivated.').ok()
                    log_embed = make_log_embed(pld.msg.author, target, warn_ident)
                    await log_event(cmd.bot, pld.settings, log_embed, 'log_warnings')
                else:
                    response = GenericResponse(f'{target.name} has no {warn_id} warning.').not_found()
            else:
                response = GenericResponse('Both user tag and warning ID are needed.').error()
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Messages needed.').denied()
    await pld.msg.channel.send(embed=response)
