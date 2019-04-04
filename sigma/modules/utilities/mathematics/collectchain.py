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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.utilities.mathematics.collector_clockwork import add_to_queue, get_queue_size
from sigma.modules.utilities.mathematics.collector_clockwork import check_queued, get_channel, get_target


async def is_blocked(db: Database, target: discord.Member, author: discord.Member):
    """

    :param db:
    :type db:
    :param target:
    :type target:
    :param author:
    :type author:
    :return:
    :rtype:
    """
    if target.id == author.id:
        blocked = False
    else:
        blocked = bool(await db[db.db_nam].BlockedChains.find_one({'user_id': target.id}))
    return blocked


async def is_blinded(db: Database, channel: discord.TextChannel, author: discord.Member):
    """

    :param db:
    :type db:
    :param channel:
    :type channel:
    :param author:
    :type author:
    :return:
    :rtype:
    """
    if author.permissions_in(channel).manage_channels:
        blinded = False
    else:
        blinded = bool(await db[db.db_nam].BlindedChains.find_one({'channel_id': channel.id}))
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
    blocked = await is_blocked(cmd.db, target_usr, pld.msg.author)
    blinded = await is_blinded(cmd.db, target_chn, pld.msg.author)
    if not blocked and not blinded:
        if not await check_queued(cmd.db, target_usr.id, pld.msg.author.id):
            if not target_usr.bot:
                cltr_itm = {'author_id': pld.msg.author.id, 'user_id': target_usr.id, 'channel_id': target_chn.id}
                await add_to_queue(cmd.db, cltr_itm)
                qsize = await get_queue_size(cmd.db)
                title = f'{starter} #{qsize} in the queue and will be notified when {ender} chain is done.'
                response = discord.Embed(color=0x66CC66)
                response.set_author(name=title, icon_url=user_avatar(target_usr))
            else:
                if target_usr.id == cmd.bot.user.id:
                    response = error('My chains are not interesting, trust me.')
                else:
                    response = error('I refuse to collect a chain for a bot.')
        else:
            mid = 'have a' if pld.msg.author.id == target_usr.id else 'has a'
            response = error(f'{starter} already in the queue or {mid} pending entry.')
    else:
        if blocked:
            response = error(f'Only {target_usr.name} can collect their own chain.')
        else:
            response = error(f'Chains for #{target_chn.name} have been disabled')
    await pld.msg.channel.send(embed=response)
