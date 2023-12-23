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

interaction_channel = None
interaction_reporter_running = False


async def interaction_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global interaction_reporter_running
    await get_interaction_channel(ev.bot)
    if not interaction_reporter_running and interaction_channel:
        interaction_reporter_running = True
        ev.bot.loop.create_task(interaction_reporter_cycler(ev))


async def get_interaction_channel(bot):
    """
    :type bot: sigma.core.sigma.ApexSigma
    """
    global interaction_channel
    if interaction_channel is None:
        intr_chn_id = bot.modules.commands.get('addinteraction').cfg.get('log_ch')
        if intr_chn_id:
            interaction_channel = await bot.get_channel(intr_chn_id, True)


def make_interaction_log_embed(inter_data):
    """
    :type inter_data: dict
    :rtype: discord.Embed
    """
    interaction_url = inter_data.get('url')
    interaction_id = inter_data.get('interaction_id')
    interaction_name = inter_data.get('name')
    data_desc = f'Author ID: {inter_data.get("user_id")}'
    data_desc += f'\nGuild ID: {inter_data.get("server_id")}'
    data_desc += f'\nInteraction URL: [Here]({interaction_url})'
    data_desc += f'\nInteraction ID: {interaction_id}'
    response_title = f'🆙 Added a new {interaction_name.lower()}'
    response = discord.Embed(color=0x3B88C3)
    response.add_field(name=response_title, value=data_desc)
    response.set_thumbnail(url=interaction_url)
    return response


async def send_interaction_log_message(bot, move_data):
    """
    :type bot: sigma.core.sigma.ApexSigma
    :type move_data: dict
    :rtype: discord.Message
    """
    await get_interaction_channel(bot)
    if interaction_channel:
        response = make_interaction_log_embed(move_data)
        # noinspection PyUnresolvedReferences
        intr_msg = await interaction_channel.send(embed=response)
        return intr_msg


async def interaction_reporter_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            interaction_docs = await ev.db.col.Interactions.find({'reported': False}).to_list(None)
            for interaction_doc in interaction_docs:
                if not interaction_channel:
                    await get_interaction_channel(ev.bot)
                log_msg = await send_interaction_log_message(ev.bot, interaction_doc)
                update_dict = {'$set': {'reported': True, 'message_id': log_msg.id if log_msg else None}}
                await ev.db.col.Interactions.update_one(interaction_doc, update_dict)
                await asyncio.sleep(1)
        await asyncio.sleep(1)
