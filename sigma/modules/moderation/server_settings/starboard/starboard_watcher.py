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
from discord.raw_models import RawReactionActionEvent

from sigma.core.sigma import ApexSigma
from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar, get_image_colors

starboard_cache = Cacher()


async def post_starboard(msg: discord.Message, response: discord.Embed, sbc: int):
    channel = msg.guild.get_channel(sbc)
    if channel:
        try:
            await channel.send(embed=response)
        except Exception:
            pass


async def generate_embed(msg: discord.Message):
    avatar = user_avatar(msg.author)
    user_color = await get_image_colors(avatar)
    response = discord.Embed(color=user_color, timestamp=arrow.utcnow().datetime)
    response.set_author(name=msg.author.name, icon_url=avatar)
    response.set_footer(text=f'#{msg.channel.name}')
    response.description = msg.content
    return response


async def check_emotes(bot: ApexSigma, msg: discord.Message, sbc: int, sbe: discord.Emoji, sbl: int):
    bid = bot.user.id
    emote_count = 0
    for reaction in msg.reactions:
        if reaction.emoji == sbe:
            async for emoji_author in reaction.users():
                if emoji_author.id != bid:
                    emote_count += 1
    if emote_count >= sbl:
        response = await generate_embed(msg)
        await post_starboard(msg, response, sbc)


async def starboard_watcher(ev: SigmaEvent, payload: RawReactionActionEvent):
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = ev.bot.get_channel(cid)
    if channel:
        guild = channel.guild
        if guild:
            starboard_doc = starboard_cache.get_cache(guild.id)
            if not starboard_doc:
                starboard_doc = await ev.db.get_guild_settings(guild.id, 'starboard')
                if starboard_doc:
                    starboard_cache.set_cache(guild.id, starboard_doc)
            if starboard_doc:
                sbc = starboard_doc.get('channel_id')
                sbe = starboard_doc.get('emote')
                sbl = starboard_doc.get('limit')
                if sbc and sbe and sbl:
                    if emoji.name == sbe:
                        user = discord.utils.find(lambda u: u.id == uid and u.guild.id == guild.id, guild.members)
                        if user:
                            if not user.bot:
                                message = await channel.get_message(mid)
                                if message:
                                    if ev.event_type == 'raw_reaction_add':
                                        try:
                                            await check_emotes(ev.bot, message, sbc, sbe, sbl)
                                        except (discord.NotFound, discord.Forbidden):
                                            pass
