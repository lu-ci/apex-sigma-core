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

system_channel = None
system_reporter_running = False


async def get_system_channel(bot):
    """
    :type bot: sigma.core.sigma.ApexSigma
    """
    global system_channel
    sys_chn_id = bot.cfg.pref.syslog_channel
    if bot.cfg.pref.syslog_channel and not system_channel:
        if sys_chn_id:
            system_channel = await bot.get_channel(sys_chn_id, True)


async def system_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global system_reporter_running
    await get_system_channel(ev.bot)
    if not system_reporter_running and system_channel:
        system_reporter_running = True
        ev.bot.loop.create_task(system_reporter_clockwork(ev))


def make_system_log_embed(data):
    """
    :type data: dict
    :rtype: discord.Embed
    """
    response = discord.Embed(title=data.get('title'), color=data.get('color'))
    response.description = data.get('content')
    return response


async def send_system_log_message(bot, data):
    """
    :type bot: sigma.core.sigma.ApexSigma
    :type data: dict
    """
    await get_system_channel(bot)
    if system_channel:
        response = make_system_log_embed(data)
        # noinspection PyUnresolvedReferences
        await system_channel.send(embed=response)


async def system_reporter_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            system_docs = await ev.db[ev.db.db_nam].SystemMessages.find({'reported': False}).to_list(None)
            for system_doc in system_docs:
                if not system_channel:
                    await get_system_channel(ev.bot)
                await send_system_log_message(ev.bot, system_doc)
                await ev.db[ev.db.db_nam].SystemMessages.update_one(system_doc, {'$set': {'reported': True}})
                await asyncio.sleep(1)
        await asyncio.sleep(1)
