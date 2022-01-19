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

from io import BytesIO

import aiohttp
import arrow
import discord

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig
from sigma.core.utilities.data_processing import get_image_colors, user_avatar

star_cache = None


async def post_starboard(msg, file, content, response, sbc):
    """
    :type msg: discord.Message
    :type file: discord.File
    :type content: str
    :type response: discord.Embed
    :type sbc: int
    """
    channel = msg.guild.get_channel(sbc)
    if channel:
        # noinspection PyBroadException
        try:
            await channel.send(file=file, content=content, embed=response)
        except Exception:
            pass


async def generate_embed(msg):
    """
    :type msg: discord.Message
    :rtype: discord.File, str, discord.Embed
    """
    avatar = user_avatar(msg.author)
    user_color = await get_image_colors(avatar)
    response = discord.Embed(color=user_color, timestamp=arrow.utcnow().datetime)
    response.set_author(name=msg.author.name, icon_url=avatar)
    response.set_footer(text=f'#{msg.channel.name}')
    response.description = msg.content

    att, file, content = None, None, None
    if msg.attachments:
        img_exts = ['png', 'jpg', 'gif', 'webp']
        vid_exts = ['webm', 'mp4']
        file_ext = msg.attachments[0].filename.lower().split('.')[-1]

        if file_ext in img_exts:
            att = True
            response.set_image(url=msg.attachments[0].url)

        elif file_ext in vid_exts:
            async with aiohttp.ClientSession() as session:
                async with session.get(msg.attachments[0].url) as resp:
                    data = await resp.read()

            response = None
            file = discord.File(BytesIO(data), f'{msg.id}.{file_ext}')
            content = f'**{msg.author.name}** in {msg.channel.mention}'

    if not any([msg.content, att, file]):
        return None, None
    return file, content, response,


# noinspection PyUnresolvedReferences
async def check_emotes(mid, uid, sbl):
    """
    :type mid: int
    :type uid: int
    :type sbl: int
    :rtype: bool
    """

    trigger = False
    executed = await star_cache.get_cache(f'exec_{mid}')
    if not executed:
        stars = await star_cache.get_cache(f'sbem_{mid}') or []
        if uid not in stars:
            stars.append(uid)
        if len(stars) >= sbl:
            trigger = True
            await star_cache.del_cache(f'sbem_{mid}')
            await star_cache.set_cache(f'exec_{mid}', True)
        else:
            await star_cache.set_cache(f'sbem_{mid}', stars)
    return trigger


async def starboard_watcher(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.RawReactionPayload
    """
    global star_cache
    if not star_cache:
        star_cache = MemoryCacher(CacheConfig({}))
    payload = pld.raw
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = await ev.bot.get_channel(cid)
    try:
        guild = channel.guild
    except AttributeError:
        guild = None
    if guild:
        starboard_doc = await ev.db.get_guild_settings(guild.id, 'starboard') or {}
        if starboard_doc.get('state'):
            sbc = starboard_doc.get('channel_id')
            sbe = starboard_doc.get('emote')
            sbl = starboard_doc.get('limit')
            if sbc and sbe and sbl:
                if channel.id != sbc:
                    if emoji.name == sbe:
                        user = guild.get_member(uid)
                        if user:
                            if not user.bot:
                                try:
                                    enough = await check_emotes(mid, uid, sbl)
                                    if enough:
                                        message = await channel.fetch_message(mid)
                                        if not message.author.bot:
                                            file, content, embed = await generate_embed(message)
                                            if file or embed:
                                                await post_starboard(message, file, content, embed, sbc)
                                except (discord.NotFound, discord.Forbidden):
                                    pass
