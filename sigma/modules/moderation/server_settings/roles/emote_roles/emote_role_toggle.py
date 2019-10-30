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


def user_has_role(role, user_roles):
    """
    Checks if a user has a specific role.
    :param role: The role to check.
    :type role: discord.Role
    :param user_roles: A list of the user's roles.
    :type user_roles: list[discord.Role]
    :return:
    :rtype: bool
    """
    has = False
    for user_role in user_roles:
        if user_role.id == role.id:
            has = True
            break
    return has


async def check_emotes(bot, msg, togglers):
    """
    Ensures only the correct reactions are present on the message.
    :param bot: The core client class.
    :type bot: sigma.core.sigma.ApexSigma
    :param msg: The message to process.
    :type msg: discord.Message
    :param togglers: A dict of emote:role_id pairs.
    :type togglers: dict
    """
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


async def emote_role_toggle(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.RawReactionPayload
    """
    payload = pld.raw
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = await ev.bot.get_channel(cid)
    if hasattr(channel, 'guild'):
        guild = channel.guild
        if guild:
            guild_togglers = await ev.db.get_guild_settings(guild.id, 'emote_role_togglers') or {}
            if guild_togglers:
                user = guild.get_member(uid)
                if user:
                    if not user.bot:
                        try:
                            message = await channel.fetch_message(mid)
                        except (discord.NotFound, discord.Forbidden):
                            message = None
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
