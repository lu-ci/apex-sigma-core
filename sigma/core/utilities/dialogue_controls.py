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
import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.professions.nodes.item_object import SigmaRawItem
from sigma.modules.minigames.utils.ongoing.ongoing import del_ongoing, is_ongoing, set_ongoing

bool_reacts = ['✅', '❌']
int_reacts = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']

errbed = error('Failed generating dialogue embed.')
errbed.description = 'Please make sure I can embed links and add reactions.'


async def ongoing_error(msg):
    # noinspection PyBroadException
    try:
        await msg.add_reaction('💬')
    except Exception:
        pass


async def bool_dialogue(bot, msg, question, tracked=False):
    """
    Creates an interactive bool dialogue message for a user to react to.
    :param bot: The bot instance associated with this message.
    :type bot: sigma.core.sigma.ApexSigma
    :param msg: The message object to reply to.
    :type msg: discord.Message
    :param question: The embed object to display the interactive bool on.
    :type question: discord.Embed
    :param tracked: Whether or not this usage is logged.
    :type tracked: bool
    :return:
    :rtype: (bool, bool)
    """
    ongoing = is_ongoing('dialogue', msg.author.id)
    if not ongoing:
        set_ongoing('dialogue', msg.author.id)
        question.set_author(name=msg.author.display_name, icon_url=user_avatar(msg.author))
        # noinspection PyBroadException
        try:
            confirmation = await msg.channel.send(embed=question)
            [await confirmation.add_reaction(preac) for preac in bool_reacts]
        except Exception:
            del_ongoing('dialogue', msg.author.id)
            await msg.channel.send(embed=errbed)
            return False, False

        def check_emote(reac, usr):
            """
            Checks for a valid message reaction.
            :param reac: The reaction to validate.
            :type reac: discord.Reaction
            :param usr: The user who reacted to the message.
            :type usr: discord.Member
            :return:
            :rtype: bool
            """
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
            timeout = False
            if ae.emoji == '✅':
                success = True
            else:
                success = False
        except asyncio.TimeoutError:
            success = False
            timeout = True
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        del_ongoing('dialogue', msg.author.id)
    else:
        await ongoing_error(msg)
        success = False
        timeout = False
    return success, timeout


async def int_dialogue(bot, msg, question, start, end):
    """
    Creates an interactive int dialogue message for a user to react to.
    :param bot: The bot instance associated with this message.
    :type bot: sigma.core.sigma.ApexSigma
    :param msg: The message object to reply to.
    :type msg: discord.Message
    :param question: The embed object to display the interactive int on.
    :type question: discord.Embed
    :param start: The number to start the range at.
    :type start: int
    :param end: The number to end the range at.
    :type end: int
    :return:
    :rtype: (int, bool)
    """
    ongoing = is_ongoing('dialogue', msg.author.id)
    if not ongoing:
        set_ongoing('dialogue', msg.author.id)
        start = 0 if start < 0 else start
        end = 9 if end > 9 else end
        question.set_author(name=msg.author.display_name, icon_url=user_avatar(msg.author))
        # noinspection PyBroadException
        try:
            confirmation = await msg.channel.send(embed=question)
            [await confirmation.add_reaction(int_reacts[preac]) for preac in range(start, end + 1)]
        except Exception:
            del_ongoing('dialogue', msg.author.id)
            await msg.channel.send(embed=errbed)
            return None, False

        def check_emote(reac, usr):
            """
            Checks for a valid message reaction.
            :param reac: The reaction to validate.
            :type reac: discord.Reaction
            :param usr: The user who reacted to the message.
            :type usr: discord.Member
            :return:
            :rtype: bool
            """
            same_author = usr.id == msg.author.id
            same_message = reac.message.id == confirmation.id
            valid_reaction = str(reac.emoji) in int_reacts
            return same_author and same_message and valid_reaction

        try:
            ae, au = await bot.wait_for('reaction_add', timeout=60, check=check_emote)
            timeout = False
            number = None
            for react_index, int_react in enumerate(int_reacts):
                if int_react == str(ae.emoji):
                    number = react_index
                    break
        except asyncio.TimeoutError:
            number = None
            timeout = True
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        del_ongoing('dialogue', msg.author.id)
    else:
        await ongoing_error(msg)
        number = None
        timeout = False
    return number, timeout


async def item_dialogue(bot, msg, icons, item: SigmaRawItem):
    """
    Creates an interactive item dialogue message for a user to react to.
    :param bot: The bot instance associated with this message.
    :type bot: sigma.core.sigma.ApexSigma
    :param msg: The message object to reply to.
    :type msg: discord.Message
    :param icons: The icons to display on the message.
    :type icons: dict
    :param item: The item to base the item dialogue on.
    :type item: sigma.modules.minigames.professions.nodes.item_object.SigmaRawItem
    :return:
    :rtype: (bool, bool)
    """
    ongoing = is_ongoing('dialogue', msg.author.id)
    if not ongoing:
        set_ongoing('dialogue', msg.author.id)
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
        # noinspection PyBroadException
        try:
            confirmation = await msg.channel.send(embed=question)
            [await confirmation.add_reaction(preac) for preac in possible]
        except Exception:
            del_ongoing('dialogue', msg.author.id)
            await msg.channel.send(embed=errbed)
            return False, False

        def check_emote(reac, usr):
            """
            Checks for a valid message reaction.
            :param reac: The reaction to validate.
            :type reac: discord.Reaction
            :param usr: The user who reacted to the message.
            :type usr: discord.Member
            :return:
            :rtype: bool
            """
            same_author = usr.id == msg.author.id
            same_message = reac.message.id == confirmation.id
            valid_reaction = str(reac.emoji) in possible
            return same_author and same_message and valid_reaction

        log_usr = f'{msg.author.name}#{msg.author.discriminator} [{msg.author.id}]'

        try:
            start_stamp = arrow.utcnow().float_timestamp
            ae, au = await bot.wait_for('reaction_add', timeout=60, check=check_emote)
            end_stamp = arrow.utcnow().float_timestamp
            bot.log.info(f'ITEM DIALOGUE: {log_usr} responded in {round(end_stamp - start_stamp, 5)}s.')
            timeout = False
            if ae.emoji == item.icon:
                success = True
            else:
                success = False
        except asyncio.TimeoutError:
            success = False
            timeout = True
            bot.log.info(f'ITEM DIALOGUE: {log_usr} timed out.')
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        del_ongoing('dialogue', msg.author.id)
    else:
        await ongoing_error(msg)
        success = False
        timeout = False
    return success, timeout
