# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

exp_clock_running = False

exp_storage = []


def add_exp(message, amount):
    global exp_storage
    storage_item = discord.utils.find(lambda x: x[0].id == message.author.id, exp_storage)
    curr_exp = storage_item[2] if storage_item else 0
    new_exp = curr_exp + amount
    exp_storage = list(filter(lambda x: x[0].id != message.author.id, exp_storage))
    exp_storage.append([message, new_exp])


async def experience_clock(ev: SigmaEvent):
    global exp_clock_running
    if not exp_clock_running:
        exp_clock_running = True
        ev.bot.loop.create_task(exp_clock_cycler(ev))


async def exp_clock_cycler(ev: SigmaEvent):
    global exp_storage
    trigger = 'message_experience'
    while True:
        if ev.bot.is_ready():
            for exp_item in [ex for ex in exp_storage]:
                message, amount = exp_item
                author = message.author
                await ev.db.add_resource(author.id, 'experience', amount, trigger, message, True)
            exp_storage = []
        await asyncio.sleep(300)
