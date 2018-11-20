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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import RawReactionPayload
from sigma.core.sigma import ApexSigma


def user_has_role(role, user_roles):
    has = False
    for user_role in user_roles:
        if user_role.id == role.id:
            has = True
            break
    return has


async def check_emotes(bot: ApexSigma, msg: discord.Message, togglers: dict):
    bid = bot.user.id
    present_emoji = []
    for reaction in msg.reactions:
        if reaction.emoji in togglers:
            present_emoji.append(reaction.emoji)
        async for emoji_author in reaction.users():
            if emoji_author.id != bid:
                await msg.remove_reaction(reaction.emoji, emoji_author)
    for toggler in togglers:
        if toggler not in present_emoji:
            await msg.add_reaction(toggler)


async def emote_role_toggle(ev: SigmaEvent, pld: RawReactionPayload):
    payload = pld.raw
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = await ev.bot.get_channel(cid)
    if channel:
        if hasattr(channel, 'guild'):
            guild = channel.guild
            if guild:
                guild_togglers = await ev.db.get_guild_settings(guild.id, 'emote_role_togglers') or {}
                if guild_togglers:
                    user = guild.get_member(uid)
                    if user:
                        if not user.bot:
                            message = await channel.get_message(mid)
                            if message:
                                smid = str(mid)
                                if smid in guild_togglers:
                                    if ev.event_type == 'raw_reaction_add':
                                        try:
                                            await check_emotes(ev.bot, message, guild_togglers.get(smid))
                                        except (discord.NotFound, discord.Forbidden):
                                            pass
                                    role_id = guild_togglers.get(smid).get(emoji.name)
                                    if role_id:
                                        role_item = guild.get_role(role_id)
                                        if role_item:
                                            if user_has_role(role_item, user.roles):
                                                await user.remove_roles(role_item, reason='Emote toggled.')
                                            else:
                                                await user.add_roles(role_item, reason='Emote toggled.')
