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

import discord

whisper_reporter_running = False


async def whisper_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global whisper_reporter_running
    if not whisper_reporter_running:
        whisper_reporter_running = True
        ev.bot.loop.create_task(whisper_reporter_clockwork(ev))


async def send_whisper_message(ev, whisper_doc):
    """

    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param whisper_doc: The whisper data to be parsed.
    :type whisper_doc: dict
    """
    whisper_chn_id = whisper_doc.get('channel_id')
    whisper_channel = await ev.bot.get_channel(whisper_chn_id)
    if whisper_channel:
        response = discord.Embed(title='😶 Incoming Whisper', description=whisper_doc.get('whisper'))
        try:
            await whisper_channel.send(embed=response)
        except (discord.Forbidden, discord.NotFound):
            pass
        await ev.db[ev.db.db_nam].Whispers.update_one(whisper_doc, {'$set': {'reported': True}})


async def whisper_reporter_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            whisper_docs = await ev.db[ev.db.db_nam].Whispers.find({'reported': False}).to_list(None)
            for whisper_doc in whisper_docs:
                await send_whisper_message(ev, whisper_doc)
                await asyncio.sleep(1)
        await asyncio.sleep(1)
