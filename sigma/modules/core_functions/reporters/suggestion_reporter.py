# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018 Lucia's Cipher
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

import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.sigma import ApexSigma

suggestion_chn_cache = None
suggestion_reporter_running = False


def make_sugg_embed(data: dict):
    usr = data.get('user')
    sgg = data.get('suggestion')
    gld = data.get('guild')
    icon = gld.get('icon') or usr.get('avatar')
    sugg_embed = discord.Embed(color=usr.get('color'), timestamp=arrow.get(data.get('timestamp')).datetime)
    sugg_embed.description = sgg.get('text')
    author_name = f'{usr.get("name")} [{usr.get("id")}]'
    footer_content = f'[{sgg.get("id")}] From {gld.get("name")}.'
    sugg_embed.set_author(name=author_name, icon_url=usr.get('avatar'))
    sugg_embed.set_footer(icon_url=icon, text=footer_content)
    return sugg_embed


async def get_suggestion_channel(bot: ApexSigma):
    global suggestion_chn_cache
    suggestion_chn = None or suggestion_chn_cache
    if suggestion_chn is None:
        sugg_chn_id = bot.modules.commands.get('botsuggest').cfg.get('channel')
        if sugg_chn_id:
            suggestion_chn_cache = suggestion_chn = await bot.get_channel(sugg_chn_id, True)
    return suggestion_chn


async def suggestion_reporter(ev: SigmaEvent):
    global suggestion_reporter_running
    suggestion_channel = await get_suggestion_channel(ev.bot)
    if not suggestion_reporter_running and suggestion_channel:
        suggestion_reporter_running = True
        ev.bot.loop.create_task(suggestion_reporter_clockwork(ev))


async def send_suggestion_log_message(bot: ApexSigma, sugg_data: dict):
    sugg_chn = await get_suggestion_channel(bot)
    sugg_msg = await sugg_chn.send(embed=make_sugg_embed(sugg_data))
    [await sugg_msg.add_reaction(r) for r in ['⬆', '⬇']]
    return sugg_msg


async def suggestion_reporter_clockwork(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            suggestion_docs = await ev.db[ev.db.db_nam].Suggestions.find({'reported': False}).to_list(None)
            for suggestion_doc in suggestion_docs:
                log_msg = await send_suggestion_log_message(ev.bot, suggestion_doc)
                update_dict = {'$set': {'reported': True, 'message': log_msg.id if log_msg else None}}
                await ev.db[ev.db.db_nam].Suggestions.update_one(suggestion_doc, update_dict)
                await asyncio.sleep(1)
        await asyncio.sleep(1)
