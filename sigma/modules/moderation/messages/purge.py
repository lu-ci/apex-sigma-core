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
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import permission_denied


def generate_log_embed(message, target, channel, deleted):
    response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'#{channel.name} Has Been Pruned', icon_url=user_avatar(message.author))
    target_text = f'{target.mention}\n{target.name}#{target.discriminator}' if target else 'No Filter'
    response.add_field(name='🗑 Prune Details', value=f'Amount: {len(deleted)} Messages\nTarget: {target_text}')
    author = message.author
    response.add_field(name='🛡 Responsible', value=f'{author.mention}\n{author.name}#{author.discriminator}')
    response.set_footer(text=f'channel_id: {channel.id}')
    return response


async def purge(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = permission_denied('Manage Messages')
    else:
        purge_images = 'attachments' in args
        purge_emotes = 'emotes' in args
        purge_filter = None
        for i, arg in enumerate(args):
            if arg.startswith('content:'):
                purge_filter = ' '.join([arg.split(':')[1]] + args[i + 1:])
                break
        target = cmd.bot.user
        count = 100
        if message.mentions:
            target = message.mentions[0]
            if len(args) == 2:
                try:
                    count = int(args[0])
                except ValueError:
                    count = 100
        else:
            if args:
                target = None
                try:
                    count = int(args[0])
                except ValueError:
                    count = 100
        if count > 100:
            count = 100

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
            await message.delete()
        except discord.NotFound:
            pass
        deleted = []
        try:
            if target:
                deleted = await message.channel.purge(limit=count, check=purge_target_check)
            else:
                deleted = await message.channel.purge(limit=count, check=purge_wide_check)
        except Exception:
            pass
        response = discord.Embed(color=0x77B255, title=f'✅ Deleted {len(deleted)} Messages')
        log_embed = generate_log_embed(message, target, message.channel, deleted)
        await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'log_purges')
    del_response = await message.channel.send(embed=response)
    await asyncio.sleep(5)
    try:
        await del_response.delete()
    except discord.NotFound:
        pass
