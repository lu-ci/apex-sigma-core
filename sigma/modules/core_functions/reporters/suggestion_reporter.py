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

suggestion_channel = None
suggestion_reporter_running = False


async def get_suggestion_channel(bot: ApexSigma):
    """

    :param bot:
    :type bot:
    """
    global suggestion_channel
    if suggestion_channel is None:
        sugg_chn_id = bot.modules.commands.get('botsuggest').cfg.get('channel')
        if sugg_chn_id:
            suggestion_channel = await bot.get_channel(sugg_chn_id, True)


async def suggestion_reporter(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global suggestion_reporter_running
    await get_suggestion_channel(ev.bot)
    if not suggestion_reporter_running and suggestion_channel:
        suggestion_reporter_running = True
        ev.bot.loop.create_task(suggestion_reporter_clockwork(ev))


def make_suggestion_log_embed(data: dict):
    """

    :param data:
    :type data:
    :return:
    :rtype:
    """
    usr = data.get('user')
    sgg = data.get('suggestion')
    gld = data.get('guild')
    icon = gld.get('icon') or usr.get('avatar')
    response = discord.Embed(color=usr.get('color'), timestamp=arrow.get(data.get('timestamp')).datetime)
    response.description = sgg.get('text')
    author_name = f'{usr.get("name")} [{usr.get("id")}]'
    footer_content = f'[{sgg.get("id")}] From {gld.get("name")}.'
    response.set_author(name=author_name, icon_url=usr.get('avatar'))
    response.set_footer(icon_url=icon, text=footer_content)
    return response


async def send_suggestion_log_message(bot: ApexSigma, sugg_data: dict):
    """

    :param bot:
    :type bot:
    :param sugg_data:
    :type sugg_data:
    :return:
    :rtype:
    """
    await get_suggestion_channel(bot)
    if suggestion_channel:
        response = make_suggestion_log_embed(sugg_data)
        sugg_msg = await suggestion_channel.send(embed=response)
        [await sugg_msg.add_reaction(r) for r in ['⬆', '⬇']]
        return sugg_msg


async def suggestion_reporter_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            suggestion_docs = await ev.db[ev.db.db_nam].Suggestions.find({'reported': False}).to_list(None)
            for suggestion_doc in suggestion_docs:
                if not suggestion_channel:
                    await get_suggestion_channel(ev.bot)
                log_msg = await send_suggestion_log_message(ev.bot, suggestion_doc)
                update_dict = {'$set': {'reported': True, 'message': log_msg.id if log_msg else None}}
                await ev.db[ev.db.db_nam].Suggestions.update_one(suggestion_doc, update_dict)
                await asyncio.sleep(1)
        await asyncio.sleep(1)
