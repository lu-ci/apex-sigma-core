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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.modules.moderation.server_settings.filters.cleaners import clean_content
from sigma.modules.moderation.warning.issuewarning import warning_data


async def edit_word_blocker(ev: SigmaEvent, before, after):
    if after.guild:
        if isinstance(after.author, discord.Member):
            is_owner = after.author.id in ev.bot.cfg.dsc.owners
            if not after.author.permissions_in(after.channel).administrator or is_owner:
                prefix = await ev.db.get_prefix(after)
                if not after.content.startswith(prefix):
                    text = clean_content(after.content.lower())
                    elements = text.split(' ')
                    blocked_words = await ev.db.get_guild_settings(after.guild.id, 'BlockedWords') or []
                    hard_blocked_words = await ev.db.get_guild_settings(after.guild.id, 'HardBlockedWords') or []
                    remove = False
                    reason = None
                    for word in blocked_words:
                        if word in elements:
                            remove = True
                            reason = word
                            break
                    for word in hard_blocked_words:
                        if word in after.content:
                            remove = True
                            reason = word
                    if remove:
                        try:
                            filter_warn = await ev.db.get_guild_settings(after.guild.id, 'FilterAutoWarn')
                            if filter_warn:
                                warn_data = warning_data(after.guild.me, after.author, f'Said "{reason}".')
                                await ev.db[ev.db.db_cfg.database].Warnings.insert_one(warn_data)
                            await after.delete()
                            title = f'🔥 Your message was deleted for containing "{reason}".'
                            to_author = discord.Embed(color=0xFFCC4D, title=title)
                            try:
                                await after.author.send(embed=to_author)
                            except discord.Forbidden:
                                pass
                            author = f'{after.author.name}#{after.author.discriminator}'
                            title = f'I deleted {author}\'s message for containing "{reason}".'
                            log_embed = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
                            log_embed.description = f'Content: {after.content}'
                            log_embed.set_author(name=title, icon_url=user_avatar(after.author))
                            log_embed.set_footer(text=f'Channel: #{after.channel.name} [{after.channel.id}]')
                            await log_event(ev.bot, after.guild, ev.db, log_embed, 'LogFilters')
                        except discord.ClientException:
                            pass
