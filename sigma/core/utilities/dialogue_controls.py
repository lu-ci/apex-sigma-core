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
import secrets

import arrow
import discord

from sigma.core.sigma import ApexSigma
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_object import SigmaRawItem

bool_reacts = ['✅', '❌']
int_reacts = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']


async def bool_dialogue(bot: ApexSigma, msg: discord.Message, question: discord.Embed, tracked: bool = False):
    question.set_author(name=msg.author.display_name, icon_url=user_avatar(msg.author))
    confirmation = await msg.channel.send(embed=question)
    [await confirmation.add_reaction(preac) for preac in bool_reacts]

    def check_emote(reac, usr):
        same_author = usr.id == msg.author.id
        same_message = reac.message.id == confirmation.id
        valid_reaction = str(reac.emoji) in bool_reacts
        return same_author and same_message and valid_reaction

    try:
        start_stamp = arrow.utcnow().float_timestamp
        ae, au = await bot.wait_for('reaction_add', timeout=60, check=check_emote)
        end_stamp = arrow.utcnow().float_timestamp
        if tracked:
            log_usr = f'{msg.author.name}#{msg.author.discriminator} [{msg.author.id}]'
            bot.log.info(f'BOOL DIALOGUE: {log_usr} responded in {round(end_stamp - start_stamp, 5)}s.')
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        if ae.emoji == '✅':
            success = True
        else:
            success = False
    except asyncio.TimeoutError:
        success = False
    return success


async def int_dialogue(bot: ApexSigma, msg: discord.Message, question: discord.Embed, start: int, end: int):
    start = 0 if start < 0 else start
    end = 9 if end > 9 else end
    question.set_author(name=msg.author.display_name, icon_url=user_avatar(msg.author))
    confirmation = await msg.channel.send(embed=question)
    [await confirmation.add_reaction(int_reacts[preac]) for preac in range(start, end)]

    def check_emote(reac, usr):
        same_author = usr.id == msg.author.id
        same_message = reac.message.id == confirmation.id
        valid_reaction = str(reac.emoji) in int_reacts
        return same_author and same_message and valid_reaction

    try:
        ae, au = await bot.wait_for('reaction_add', timeout=60, check=check_emote)
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        number = None
        for react_index, int_react in enumerate(int_reacts):
            if int_react == str(ae.emoji):
                number = react_index
                break
    except asyncio.TimeoutError:
        number = None
    return number


async def item_dialogue(bot: ApexSigma, msg: discord.Message, icons: dict, item: SigmaRawItem):
    icon_list = [icons.get(ic) for ic in icons if icons.get(ic) != item.icon]
    icon_list.pop(0)
    possible_proto = [item.icon]
    while len(possible_proto) < secrets.randbelow(2) + 3:
        possible_proto.append(icon_list.pop(secrets.randbelow(len(icon_list))))
    possible = []
    while possible_proto:
        possible.append(possible_proto.pop(secrets.randbelow(len(possible_proto))))
    question = discord.Embed(color=item.color, title=f'{item.icon} Quick! Get the correct {item.type.lower()}!')
    question.set_author(name=msg.author.display_name, icon_url=user_avatar(msg.author))
    confirmation = await msg.channel.send(embed=question)
    [await confirmation.add_reaction(preac) for preac in possible]

    def check_emote(reac, usr):
        same_author = usr.id == msg.author.id
        same_message = reac.message.id == confirmation.id
        valid_reaction = str(reac.emoji) in possible
        return same_author and same_message and valid_reaction

    try:
        ae, au = await bot.wait_for('reaction_add', timeout=60, check=check_emote)
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        timeout = False
        if ae.emoji == item.icon:
            success = True
        else:
            success = False
    except asyncio.TimeoutError:
        success = False
        timeout = True
    return success, timeout
