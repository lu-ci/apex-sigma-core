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

import asyncio

import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload


async def afk_mention_check(ev: SigmaEvent, pld: MessagePayload):
    if pld.msg.guild:
        pfx = ev.db.get_prefix(pld.settings)
        if not pld.msg.content.startswith(pfx):
            if pld.msg.mentions:
                target = pld.msg.mentions[0]
                afk_data = await ev.db.cache.get_cache(f'afk_{pld.msg.author.id}')
                if not afk_data:
                    afk_data = await ev.db[ev.db.db_nam].AwayUsers.find_one({'user_id': target.id})
                if afk_data:
                    time_then = arrow.get(afk_data.get('timestamp', 0))
                    afk_time = arrow.get(time_then).humanize(arrow.utcnow()).title()
                    afk_reason = afk_data.get('reason')
                    url = None
                    for piece in afk_reason.split():
                        if piece.startswith('http'):
                            suffix = piece.split('.')[-1]
                            if suffix in ['gif', 'jpg', 'jpeg', 'png']:
                                afk_reason = afk_reason.replace(piece, '') if afk_reason is not None else afk_reason
                                url = piece
                                break
                    response = discord.Embed(color=0x3B88C3, timestamp=time_then.datetime)
                    reason = f'Reason: {afk_reason}\nWent AFK: {afk_time}'
                    response.add_field(name=f'ℹ {target.name} is AFK.', value=reason)
                    if url:
                        response.set_image(url=url)
                    afk_notify = await pld.msg.channel.send(embed=response)
                    await asyncio.sleep(5)
                    try:
                        await afk_notify.delete()
                    except discord.NotFound:
                        pass
