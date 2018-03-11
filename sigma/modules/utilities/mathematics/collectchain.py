# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from .collector_clockwork import check_queued, get_target, get_channel, get_queue_size, add_to_queue


class CollectorItem(object):
    def __init__(self, ath, usr, chn):
        self.ath = ath
        self.usr = usr
        self.chn = chn


async def collectchain(cmd: SigmaCommand, message: discord.Message, args: list):
    target_usr = get_target(message)
    starter = 'You are' if message.author.id == target_usr.id else f'{target_usr.name} is'
    ender = 'your' if message.author.id == target_usr.id else 'their'
    if not check_queued(target_usr.id):
        target_chn = get_channel(message)
        if not target_usr.bot:
            cltr_itm = CollectorItem(message.author, target_usr, target_chn)
            await add_to_queue(cltr_itm)
            qsize = get_queue_size()
            title = f'{starter} #{qsize} in the queue and will be notified when {ender} chain is done.'
            response = discord.Embed(color=0x66CC66)
            response.set_author(name=title, icon_url=user_avatar(target_usr))
        else:
            if target_usr.id == cmd.bot.user.id:
                response = discord.Embed(color=0xBE1931, title='❗ My chains are not interesting, trust me.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I refuse to collect a chain for a bot.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ {starter} already in the collection queue.')
    await message.channel.send(embed=response)
