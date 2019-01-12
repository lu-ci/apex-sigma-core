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
from sigma.core.mechanics.payload import MessagePayload
from sigma.core.mechanics.permissions import check_filter_perms
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.modules.moderation.server_settings.filters.cleaners import clean_content
from sigma.modules.moderation.warning.issuewarning import warning_data


async def send_word_blocker(ev: SigmaEvent, pld: MessagePayload):
    if pld.msg.guild:
        if isinstance(pld.msg.author, discord.Member):
            override = check_filter_perms(pld.msg, pld.settings, 'words')
            is_owner = pld.msg.author.id in ev.bot.cfg.dsc.owners
            if not any([pld.msg.author.guild_permissions.administrator, is_owner, override]):
                prefix = ev.db.get_prefix(pld.settings)
                if not pld.msg.content.startswith(prefix):
                    text = clean_content(pld.msg.content.lower())
                    elements = text.split(' ')
                    blocked_words = pld.settings.get('blocked_words') or []
                    hard_blocked_words = pld.settings.get('hardblocked_words') or []
                    remove = False
                    reason = None
                    for word in blocked_words:
                        if word in elements:
                            remove = True
                            reason = word
                            break
                    for word in hard_blocked_words:
                        if word in pld.msg.content:
                            remove = True
                            reason = word
                    if remove:
                        try:
                            filter_warn = pld.settings.get('filter_auto_warn')
                            if filter_warn:
                                warn_data = warning_data(pld.msg.guild.me, pld.msg.author, f'Said "{reason}".')
                                await ev.db[ev.db.db_nam].Warnings.insert_one(warn_data)
                            await pld.msg.delete()
                            title = f'🔥 Your message was deleted for containing "{reason}".'
                            to_author = discord.Embed(color=0xFFCC4D, title=title)
                            try:
                                await pld.msg.author.send(embed=to_author)
                            except discord.Forbidden:
                                pass
                            author = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                            title = f'I deleted {author}\'s message for containing "{reason}".'
                            log_embed = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
                            log_embed.description = f'Content: {pld.msg.content}'
                            log_embed.set_author(name=title, icon_url=user_avatar(pld.msg.author))
                            log_embed.set_footer(text=f'Channel: #{pld.msg.channel.name} [{pld.msg.channel.id}]')
                            await log_event(ev.bot, pld.settings, log_embed, 'log_filters')
                        except (discord.ClientException, discord.NotFound, discord.Forbidden):
                            pass
