# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import asyncio

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.sigma import ApexSigma

interaction_channel = None
interaction_reporter_running = False


async def get_interaction_channel(bot: ApexSigma):
    global interaction_channel
    if interaction_channel is None:
        intr_chn_id = bot.modules.commands.get('addinteraction').cfg.get('log_ch')
        if intr_chn_id:
            interaction_channel = await bot.get_channel(intr_chn_id, True)


async def interaction_reporter(ev: SigmaEvent):
    global interaction_reporter_running
    await get_interaction_channel(ev.bot)
    if not interaction_reporter_running and interaction_channel:
        interaction_reporter_running = True
        ev.bot.loop.create_task(interaction_reporter_clockwork(ev))


async def send_interaction_log_message(inter_data: dict):
    interaction_url = inter_data.get('url')
    interaction_id = inter_data.get('interaction_id')
    interaction_name = inter_data.get('name')
    data_desc = f'Author ID: {inter_data.get("user_id")}'
    data_desc += f'\nGuild ID: {inter_data.get("server_id")}'
    data_desc += f'\nInteraction URL: [Here]({interaction_url})'
    data_desc += f'\nInteraction ID: {interaction_id}'
    log_resp_title = f'🆙 Added a new {interaction_name.lower()}'
    log_resp = discord.Embed(color=0x3B88C3)
    log_resp.add_field(name=log_resp_title, value=data_desc)
    log_resp.set_thumbnail(url=interaction_url)
    log_msg = await interaction_channel.send(embed=log_resp)
    return log_msg


async def interaction_reporter_clockwork(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            interaction_docs = await ev.db[ev.db.db_nam].Interactions.find({'reported': False}).to_list(None)
            for interaction_doc in interaction_docs:
                if not interaction_channel:
                    await get_interaction_channel(ev.bot)
                log_msg = await send_interaction_log_message(interaction_doc)
                update_dict = {'$set': {'reported': True, 'message_id': log_msg.id if log_msg else None}}
                await ev.db[ev.db.db_nam].Interactions.update_one(interaction_doc, update_dict)
                await asyncio.sleep(1)
        await asyncio.sleep(1)
