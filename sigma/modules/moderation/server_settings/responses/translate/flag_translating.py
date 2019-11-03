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
from translate import Translator

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig
from sigma.core.utilities.generic_responses import error
from sigma.modules.moderation.server_settings.responses.translate.flag_emotes import flag_emotes

message_cache = MemoryCacher(CacheConfig({}))


async def send_translation(channel, message, translation, fr_lang, to_lang):
    title = f'🔠 Translated from {fr_lang.upper()} to {to_lang.upper()}'
    trans_embed = discord.Embed(color=0x3B88C3, title=title, description=translation)
    await channel.send(embed=trans_embed)
    await message.add_reaction('✔')


async def flag_translating(ev, pld):
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
        try:
            guild = channel.guild
        except AttributeError:
            guild = None
        if guild:
            enabled = pld.settings.get('flag_translate')
            if enabled:
                if emoji.name in flag_emotes:
                    user = guild.get_member(uid)
                    if not user or not user.permissions_in(channel).send_messages:
                        return
                    data = await message_cache.get_cache(mid)
                    if not data:
                        data = {'fr_lang': flag_emotes[emoji.name]}
                        await message_cache.set_cache(mid, data)
                    elif not data.get('executed'):
                        msg = await channel.fetch_message(mid)
                        if msg:
                            if not guild.me.permissions_in(channel).send_messages:
                                try:
                                    await msg.add_reaction('📝')
                                except (discord.NotFound, discord.Forbidden):
                                    pass
                            fr_lang = data.get('fr_lang')
                            to_lang = flag_emotes.get(emoji.name)
                            translator = Translator(to_lang=to_lang, from_lang=fr_lang)
                            translation = translator.translate(msg.content)
                            if 'is an invalid' in translation.lower():
                                await msg.add_reaction('❗')
                                return
                            # 'excedeed' is misspelled intentionally
                            elif 'length limit excedeed' in translation.lower():
                                response = error('Maximum query limit is 500 characters.')
                                await channel.send(embed=response)
                            try:
                                await send_translation(channel, msg, translation, fr_lang, to_lang)
                                data.update({'executed': True})
                                await message_cache.set_cache(mid, data)
                            except (discord.NotFound, discord.Forbidden):
                                pass
