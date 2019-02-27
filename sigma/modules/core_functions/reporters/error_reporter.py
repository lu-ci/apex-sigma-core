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

from sigma.core.mechanics.errors import SigmaError
from sigma.core.mechanics.event import SigmaEvent
from sigma.core.sigma import ApexSigma

error_chn_cache = None
error_reporter_running = False


async def get_error_channel(bot: ApexSigma):
    global error_chn_cache
    if bot.cfg.pref.errorlog_channel and error_chn_cache is None:
        err_chn_id = bot.cfg.pref.errorlog_channel
        if err_chn_id:
            error_chn_cache = await bot.get_channel(err_chn_id, True)
    return error_chn_cache


async def error_reporter(ev: SigmaEvent):
    global error_reporter_running
    error_channel = await get_error_channel(ev.bot)
    if not error_reporter_running and error_channel:
        error_reporter_running = True
        ev.bot.loop.create_task(error_reporter_clockwork(ev))


async def send_error_log(bot: ApexSigma, error_data):
    error_chn = await get_error_channel(bot)
    if error_chn and error_data:
        response, trace = SigmaError.make_error_embed(error_data)
        await error_chn.send(embed=response)
        if trace:
            await error_chn.send(trace)


async def error_reporter_clockwork(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            error_docs = await ev.db[ev.db.db_nam].Errors.find({'reported': False}).to_list(None)
            for error_doc in error_docs:
                await send_error_log(ev.bot, error_doc)
                await ev.db[ev.db.db_nam].Errors.update_one(error_doc, {'$set': {'reported': True}})
                await asyncio.sleep(1)
        await asyncio.sleep(1)
