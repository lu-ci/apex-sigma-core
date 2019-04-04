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

from sigma.core.mechanics.payload import RawReactionPayload


async def remover_detector(ev, pld: RawReactionPayload):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld:
    :type pld:
    """
    payload = pld.raw
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    if uid in ev.bot.cfg.dsc.owners:
        log_ch_id = ev.bot.modules.commands.get('addinteraction').cfg.get('log_ch')
        if cid is not None and cid == log_ch_id:
            if emoji.name == '✅':
                interaction_item = await ev.db[ev.db.db_nam].Interactions.find_one({'message_id': mid})
                if interaction_item:
                    await ev.db[ev.db.db_nam].Interactions.update_one(interaction_item, {'$set': {'active': True}})
                    channel = await ev.bot.get_channel(log_ch_id, True)
                    message = await channel.fetch_message(mid) if channel else None
                    if message:
                        await message.add_reaction('🆗')
