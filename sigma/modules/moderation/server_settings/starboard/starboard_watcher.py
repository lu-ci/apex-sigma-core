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

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar, get_image_colors


star_cache = Cacher()


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


def check_emotes(mid: int, sbl: int):
    trigger = False
    executed = star_cache.get_cache(f'exec_{mid}')
    if not executed:
        stars = star_cache.get_cache(mid) or 0
        stars += 1
        if stars >= sbl:
            trigger = True
            star_cache.del_cache(mid)
            star_cache.set_cache(f'exec_{mid}', True)
        else:
            star_cache.set_cache(mid, stars)
    return trigger


async def starboard_watcher(ev: SigmaEvent, payload: RawReactionActionEvent):
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = ev.bot.get_channel(cid)
    if channel:
        guild = channel.guild
        if guild:
            starboard_doc = await ev.db.get_guild_settings(guild.id, 'starboard') or {}
            if starboard_doc:
                sbc = starboard_doc.get('channel_id')
                sbe = starboard_doc.get('emote')
                sbl = starboard_doc.get('limit')
                if sbc and sbe and sbl:
                    if emoji.name == sbe:
                        user = guild.get_member(uid)
                        if user:
                            if not user.bot:
                                try:
                                    enough = check_emotes(mid, sbl)
                                    if enough:
                                        message = await channel.get_message(mid)
                                        response = await generate_embed(message)
                                        await post_starboard(message, response, sbc)
                                except (discord.NotFound, discord.Forbidden):
                                    pass
