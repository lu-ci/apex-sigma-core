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

from sigma.core.sigma import ApexSigma

movement_channel = None
movement_reporter_running = False


async def get_movement_channel(bot: ApexSigma):
    """

    :param bot:
    :type bot:
    """
    global movement_channel
    move_chn_id = bot.cfg.pref.movelog_channel
    if bot.cfg.pref.movelog_channel and not movement_channel:
        if move_chn_id:
            movement_channel = await bot.get_channel(move_chn_id, True)


async def movement_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global movement_reporter_running
    await get_movement_channel(ev.bot)
    if not movement_reporter_running and movement_channel:
        movement_reporter_running = True
        ev.bot.loop.create_task(movement_reporter_clockwork(ev))


def make_movement_log_embed(data: dict):
    """

    :param data:
    :type data:
    :return:
    :rtype:
    """
    joined = data.get('join')
    gld = data.get('guild', {})
    owner = data.get('owner', {})
    population = data.get("population", {})
    resp_color = 0x66CC66 if joined else 0xBE1931
    resp_title = 'Joined a Guild' if joined else 'Left a Guild'
    creation_time = arrow.get(gld.get('created_at')).format('DD. MMMM YYYY')
    guild_text = f'Name: **{gld.get("name")}**'
    guild_text += f'\nOwner: **{owner.get("name")}**#*{owner.get("discriminator")}*'
    guild_text += f'\nID: **{gld.get("id")}**'
    guild_text += f'\nCreated: **{creation_time}**'
    nums_text = f'Members: **{population.get("users")}**'
    nums_text += f'\nBots: **{population.get("bots")}**'
    nums_text += f'\nChannels: **{population.get("channels")}**'
    nums_text += f'\nRoles: **{population.get("roles")}**'
    icon = gld.get('icon') or owner.get('avatar')
    response = discord.Embed(color=resp_color)
    response.set_author(name=resp_title, icon_url=icon, url=icon)
    response.add_field(name='Guild Info', value=guild_text)
    response.add_field(name='Guild Stats', value=nums_text)
    return response


async def send_movement_log_message(bot: ApexSigma, move_data: dict):
    """

    :param bot:
    :type bot:
    :param move_data:
    :type move_data:
    """
    await get_movement_channel(bot)
    if movement_channel:
        response = make_movement_log_embed(move_data)
        await movement_channel.send(embed=response)


async def movement_reporter_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            movement_docs = await ev.db[ev.db.db_nam].Movements.find({'reported': False}).to_list(None)
            for movement_doc in movement_docs:
                if not movement_channel:
                    await get_movement_channel(ev.bot)
                await send_movement_log_message(ev.bot, movement_doc)
                await ev.db[ev.db.db_nam].Movements.update_one(movement_doc, {'$set': {'reported': True}})
                await asyncio.sleep(1)
        await asyncio.sleep(1)
