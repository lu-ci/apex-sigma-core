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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.utilities.mathematics.collector_clockwork import add_to_queue, get_queue_size, collector_limit
from sigma.modules.utilities.mathematics.collector_clockwork import check_queued, get_channel, get_target


async def is_blocked(db, target, author):
    """
    :type db: sigma.core.mechanics.database.Database
    :type target: discord.Member
    :type author: discord.Member
    :rtype: bool
    """
    if target.id == author.id:
        blocked = False
    else:
        blocked = bool(await db.col.BlockedChains.find_one({'user_id': target.id}))
    return blocked


async def is_blinded(db, channel, author):
    """
    :type db: sigma.core.mechanics.database.Database
    :type channel: discord.TextChannel
    :type author: discord.Member
    :rtype: bool
    """
    if channel.permissions_for(author).manage_channels:
        blinded = False
    else:
        blinded = bool(await db.col.BlindedChains.find_one({'channel_id': channel.id}))
    return blinded


async def collectchain(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target_usr = get_target(pld.msg)
    target_chn = get_channel(pld.msg)
    starter = 'You are' if pld.msg.author.id == target_usr.id else f'{target_usr.name} is'
    ender = 'your' if pld.msg.author.id == target_usr.id else 'their'
    if target_chn.permissions_for(pld.msg.guild.me).read_messages:
        blocked = await is_blocked(cmd.db, target_usr, pld.msg.author)
        blinded = await is_blinded(cmd.db, target_chn, pld.msg.author)
        if not blocked and not blinded:
            queue_check = await check_queued(cmd.db, target_usr.id, pld.msg.author.id)
            if not queue_check.get('queued'):
                if not target_usr.bot:
                    cltr_itm = {
                        'author_id': pld.msg.author.id,
                        'user_id': target_usr.id,
                        'channel_id': target_chn.id,
                        'stamp': arrow.utcnow().int_timestamp
                    }
                    await add_to_queue(cmd.db, cltr_itm)
                    qsize = await get_queue_size(cmd.db)
                    now = arrow.utcnow().int_timestamp
                    max_time = (collector_limit / 100) * qsize
                    max_finish = arrow.get(now + max_time)
                    title = f'{starter} #{qsize} in the queue and will be notified when {ender} chain is done.'
                    description = 'Due to Discord limitations, walking back through messages can take a long time.'
                    description += f' The maximum time until {ender} chain is done should be {max_finish.humanize()}.'
                    response = discord.Embed(color=0x66CC66)
                    response.description = description
                    response.set_author(name=title, icon_url=user_avatar(target_usr))
                else:
                    if target_usr.id == cmd.bot.user.id:
                        response = GenericResponse('My chains are not interesting, trust me.').error()
                    else:
                        response = GenericResponse('I refuse to collect a chain for a bot.').error()
            else:
                mid = 'have a' if pld.msg.author.id == target_usr.id else 'has a'
                if queue_check.get('target'):
                    description = 'A collection has already been requested for you.'
                elif queue_check.get('author'):
                    description = 'You have already requested a collection for someone.'
                else:
                    description = 'Your chain is currently being collected, please wait for it to finish.'
                document = queue_check.get('document')
                now = arrow.utcnow().int_timestamp
                timestamp = document.get('stamp')
                difference = now - timestamp
                if difference < 60:
                    description += f' It was requested **{difference} seconds** ago.'
                else:
                    elapsed = arrow.get(timestamp).humanize()
                    description += f' It was requested **{elapsed}**.'
                response = GenericResponse(f'{starter} already in the queue or {mid} pending entry.').error()
                response.description = description
        else:
            if blocked:
                response = GenericResponse(f'Only {target_usr.name} can collect their own chain.').error()
            else:
                response = GenericResponse(f'Chains for #{target_chn.name} have been disabled.').error()
    else:
        response = GenericResponse(f'I can\'t read messages in #{target_chn.name}.').error()
    await pld.msg.channel.send(embed=response)
