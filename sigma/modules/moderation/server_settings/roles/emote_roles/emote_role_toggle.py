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
import discord
from discord.raw_models import RawReactionActionEvent

from sigma.core.mechanics.event import SigmaEvent


def user_has_role(role, user_roles):
    has = False
    for user_role in user_roles:
        if user_role.id == role.id:
            has = True
            break
    return has


async def emote_role_toggle(ev: SigmaEvent, payload: RawReactionActionEvent):
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = discord.utils.find(lambda c: c.id == cid, ev.bot.get_all_channels())
    if channel:
        guild = channel.guild
        if guild:
            guild_togglers = await ev.db.get_guild_settings(guild.id, 'EmoteRoleTogglers') or {}
            if guild_togglers:
                user = discord.utils.find(lambda u: u.id == uid and u.guild.id == guild.id, guild.members)
                if user:
                    if not user.bot:
                        message = await channel.get_message(mid)
                        if message:
                            smid = str(mid)
                            if smid in guild_togglers:
                                if ev.event_type == 'raw_reaction_add':
                                    try:
                                        await message.remove_reaction(emoji.name, user)
                                    except discord.NotFound:
                                        pass
                                role_id = guild_togglers.get(smid).get(emoji.name)
                                if role_id:
                                    role_item = discord.utils.find(lambda x: x.id == role_id, guild.roles)
                                    if role_item:
                                        if user_has_role(role_item, user.roles):
                                            await user.remove_roles(role_item)
                                        else:
                                            await user.add_roles(role_item)
