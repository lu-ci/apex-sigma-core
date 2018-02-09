# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


def generate_log_embed(message, target, channel, deleted):
    response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'#{channel.name} Has Been Pruned', icon_url=user_avatar(message.author))
    if target:
        target_text = f'{target.mention}\n{target.name}#{target.discriminator}'
    else:
        target_text = 'No Filter'
    response.add_field(name='🗑 Prune Details',
                       value=f'Amount: {len(deleted)} Messages\nTarget: {target_text}',
                       inline=True)
    author = message.author
    response.add_field(name='🛡 Responsible',
                       value=f'{author.mention}\n{author.name}#{author.discriminator}',
                       inline=True)
    response.set_footer(text=f'ChannelID: {channel.id}')
    return response


async def purge(cmd: SigmaCommand, message: discord.Message, args: list):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        valid_count = True
        target = cmd.bot.user
        count = 100
        if message.mentions:
            target = message.mentions[0]
            if len(args) == 2:
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        else:
            if args:
                target = None
                try:
                    count = int(args[0])
                except ValueError:
                    valid_count = False
        if count > 100:
            count = 100
        if not valid_count:
            response = discord.Embed(color=0xBE1931, title=f'❗ {args[0]} is not a valid number.')
        else:
            def purge_target_check(msg):
                if not msg.pinned:
                    if msg.author.id == target.id:
                        clean = True
                    else:
                        clean = False
                else:
                    clean = False
                return clean

            def purge_wide_check(msg):
                if not msg.pinned:
                    clean = True
                else:
                    clean = False
                return clean

            try:
                await message.delete()
            except discord.NotFound:
                pass
            if target:
                try:
                    deleted = await message.channel.purge(limit=count, check=purge_target_check)
                except Exception:
                    deleted = []
                    pass
            else:
                try:
                    deleted = await message.channel.purge(limit=count, check=purge_wide_check)
                except Exception:
                    deleted = []
                    pass
            response = discord.Embed(color=0x77B255, title=f'✅ Deleted {len(deleted)} Messages')
            log_embed = generate_log_embed(message, target, message.channel, deleted)
            await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'LogPurges')
    del_response = await message.channel.send(embed=response)
    await asyncio.sleep(5)
    try:
        await del_response.delete()
    except discord.NotFound:
        pass
