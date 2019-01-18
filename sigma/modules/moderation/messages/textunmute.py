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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.database import Database
from sigma.core.mechanics.incident import get_incident_core
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import denied, ok, error
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name='A Member Has Been Unmuted', icon_url=user_avatar(target))
    log_embed.add_field(name='🔊 Unmuted User',
                        value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_embed.add_field(name='🛡 Responsible',
                        value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_embed.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_embed.set_footer(text=f'User ID {target.id}')
    return log_embed


async def make_incident(db: Database, gld: discord.Guild, ath: discord.Member, trg: discord.Member, reason: str):
    icore = get_incident_core(db)
    inc = icore.generate('textunmute')
    inc.set_location(gld)
    inc.set_moderator(ath)
    inc.set_target(trg)
    inc.set_reason(reason)
    await icore.save(inc)
    await icore.report(gld, inc.to_embed('🔊', 0x696969))


async def textunmute(cmd: SigmaCommand, pld: CommandPayload):
    if not pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        response = denied('Manage Messages')
    else:
        if not pld.msg.mentions:
            response = error('No user targeted.')
        else:
            author = pld.msg.author
            target = pld.msg.mentions[0]
            is_admin = author.permissions_in(pld.msg.channel).administrator
            if author.id == target.id and not is_admin:
                response = error('Can\'t unmute yourself.')
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier and not is_admin:
                    response = discord.Embed(color=0xBE1931, title='⛔ Can\'t unmute someone equal or above you.')
                else:
                    mute_list = pld.settings.get('muted_users')
                    if mute_list is None:
                        mute_list = []
                    if target.id not in mute_list:
                        resp_title = f'❗ {target.display_name} is not text muted.'
                        response = discord.Embed(color=0xBE1931, title=resp_title)
                    else:
                        mute_list.remove(target.id)
                        reason = ' '.join(pld.args[1:]) if pld.args[1:] else None
                        await make_incident(cmd.db, pld.msg.guild, pld.msg.author, target, reason)
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'muted_users', mute_list)
                        response = ok(f'{target.display_name} has been unmuted.')
                        log_embed = generate_log_embed(pld.msg, target, reason)
                        await log_event(cmd.bot, pld.settings, log_embed, 'log_mutes')
    await pld.msg.channel.send(embed=response)
