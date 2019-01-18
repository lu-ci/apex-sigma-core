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

import asyncio
import re
from unicodedata import category

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import denied, ok, error

ongoing = []


def generate_log_embed(message, target, channel, deleted):
    response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'#{channel.name} Has Been Pruned', icon_url=user_avatar(message.author))
    target_text = f'{target.mention}\n{target.name}#{target.discriminator}' if target else 'No Filter'
    response.add_field(name='🗑 Prune Details', value=f'Amount: {len(deleted)} Messages\nTarget: {target_text}')
    author_text = f'{message.author.mention}\n{message.author.name}#{message.author.discriminator}'
    response.add_field(name='🛡 Responsible', value=author_text)
    response.set_footer(text=f'ChannelID: {channel.id}')
    return response


async def purge(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        if pld.msg.channel.id not in ongoing:
            ongoing.append(pld.msg.channel.id)
            pld.args = [a.lower() for a in pld.args]
            purge_images = 'attachments' in pld.args
            purge_emotes = 'emotes' in pld.args
            until_pin = 'untilpin' in pld.args
            purge_filter = None
            for i, arg in enumerate(pld.args):
                if arg.startswith('content:'):
                    purge_filter = ' '.join([arg.split(':')[1]] + pld.args[i + 1:])
                    break

            async def get_limit_and_target():
                user = cmd.bot.user
                limit = 100
                if pld.msg.mentions:
                    user = pld.msg.mentions[0]
                    if len(pld.args) == 2:
                        try:
                            limit = int(pld.args[0])
                        except ValueError:
                            limit = 100
                else:
                    if pld.args:
                        user = None
                        try:
                            limit = int(pld.args[0])
                        except ValueError:
                            limit = 100
                if until_pin:
                    channel_hist = await pld.msg.channel.history(limit=limit).flatten()
                    for n, log in enumerate(channel_hist):
                        if log.pinned:
                            limit = n - 1
                if limit > 100:
                    limit = 100
                return limit, user

            count, target = await get_limit_and_target()

            def is_emotes(msg):
                clean = False
                if msg.content:
                    for piece in msg.content.split():
                        piece = piece.strip()
                        if re.match(r'^<a?:\w+:\d+>$', piece):
                            clean = True
                        elif re.match(r'^:\w+:$', piece):
                            clean = True
                        elif len(piece) == 1 and category(piece) == 'So':
                            clean = True
                        else:
                            clean = False
                            break
                return clean

            def purge_target_check(msg):
                clean = False
                if not msg.pinned:
                    if msg.author.id == target.id:
                        if purge_images:
                            if msg.attachments:
                                clean = True
                        elif purge_emotes:
                            clean = is_emotes(msg)
                        elif purge_filter:
                            if purge_filter.lower() in msg.content.lower():
                                clean = True
                        else:
                            clean = True
                return clean

            def purge_wide_check(msg):
                clean = False
                if not msg.pinned:
                    if purge_images:
                        if msg.attachments:
                            clean = True
                    elif purge_emotes:
                        clean = is_emotes(msg)
                    elif purge_filter:
                        if purge_filter.lower() in msg.content.lower():
                            clean = True
                    else:
                        clean = True
                return clean

            try:
                await pld.msg.delete()
            except discord.NotFound:
                pass
            deleted = []
            try:
                if target:
                    deleted = await pld.msg.channel.purge(limit=count, check=purge_target_check)
                else:
                    deleted = await pld.msg.channel.purge(limit=count, check=purge_wide_check)
            except Exception:
                pass
            response = ok(f'Deleted {len(deleted)} Messages')
            log_embed = generate_log_embed(pld.msg, target, pld.msg.channel, deleted)
            await log_event(cmd.bot, pld.settings, log_embed, 'log_purges')
            if pld.msg.channel.id in ongoing:
                ongoing.remove(pld.msg.channel.id)
            try:
                del_response = await pld.msg.channel.send(embed=response)
                await asyncio.sleep(5)
                await del_response.delete()
            except discord.NotFound:
                pass
            return
        else:
            response = error('There is already one ongoing.')
    else:
        response = denied('Manage Messages')
    await pld.msg.channel.send(embed=response)
