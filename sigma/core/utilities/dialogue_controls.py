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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

TIMEOUT = 60

CANCEL_REACT = '❌'
CONFIRM_REACT = '✅'

BOOL_REACTIONS = [CONFIRM_REACT, CANCEL_REACT]
INT_REACTIONS = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']


class DialogueResponse(object):
    """
    Handles the creation of dialogue response embeds.
    """

    def __init__(self, core):
        """
        :param core:
        :type core: DialogueCore
        """
        self.core = core
        self.ok = False
        self.cancelled = False
        self.timed_out = False
        self.ongoing = False
        self.error = False
        self.value = None

    @staticmethod
    def get_desc(desc):
        """
        Parses text so that only the first character
        of the string is capitalized.
        :param desc:
        :type desc: str
        :type desc: str
        :rtype: str
        """
        pieces = desc.split(' ')
        if len(pieces) > 1:
            first = pieces[0].title()
            other = [piece.lower() for piece in pieces[1:]]
            desc = ' '.join([first] + other)
        else:
            desc = desc.title()
        return desc

    @staticmethod
    def generic_ok(desc):
        """
        Creates a generic-success dialogue embed
        :param desc:
        :type desc: str
        :return:
        :rtype: discord.Embed
        """
        desc = DialogueResponse.get_desc(desc)
        return GenericResponse(f'{desc} dialogue confirmed.').ok()

    @staticmethod
    def generic_cancelled(desc):
        """
        Creates a generic-cancelled dialogue embed
        :param desc:
        :type desc: str
        :return:
        :rtype: discord.Embed
        """
        desc = DialogueResponse.get_desc(desc)
        return discord.Embed(color=0xbe1931, title=f'❌ {desc} dialogue cancelled.')

    @staticmethod
    def generic_timed_out(desc):
        """
        Creates a generic-timed-out dialogue embed
        :param desc:
        :type desc: str
        :return:
        :rtype: discord.Embed
        """
        desc = DialogueResponse.get_desc(desc)
        return discord.Embed(color=0x696969, title=f'🕙 {desc} dialogue timed out.')

    @staticmethod
    def generic_ongoing():
        """
        Creates a generic-ongoing dialogue embed
        :return:
        :rtype: discord.Embed
        """
        response = discord.Embed(color=0x2a6797, title='💬 Somewhere, a dialogue is already open for you.')
        response.description = "If this is incorrect and you experienced an error recently, "
        response.description += 'please use the **resetongoing** command to clear all your ongoing markers.'
        response.description += ' Things like getting items, answering questions, and confirming are all dialogues.'
        return response

    @staticmethod
    def generic_error():
        """
        Creates a generic-error dialogue embed
        :return:
        :rtype: discord.Embed
        """
        respone = GenericResponse('Failed generating the dialogue embed.').error()
        respone.description = 'Please make sure I can embed links and add reactions.'
        return respone

    @staticmethod
    def generic_unknown():
        """
        Creates a unknown-issue dialogue embed.
        :return:
        :rtype: discord.Embed
        """
        return GenericResponse('This is never supposed to happen, report it to the devs please.').warn()

    def generic(self, desc):
        """
        Returns the flagged generic dialogue embed.
        :param desc:
        :type desc: str
        :return:
        :rtype: discord.Embed
        """
        if self.ok:
            return self.generic_ok(desc)
        elif self.cancelled:
            return self.generic_cancelled(desc)
        elif self.timed_out:
            return self.generic_timed_out(desc)
        elif self.ongoing:
            return self.generic_ongoing()
        elif self.error:
            return self.generic_error()
        else:
            return self.generic_unknown()


class DialogueCore(object):
    """
    Handles the creation and processing of dialogue control embeds.
    """

    def __init__(self, bot, msg, question=None):
        """
        :param bot:
        :type bot: sigma.core.sigma.ApexSigma
        :param msg:
        :type msg:discord.Message
        :param question:
        :type question:discord.Embed or None
        """
        self.bot = bot
        self.msg = msg
        self.guild = msg.guild
        self.channel = msg.channel
        self.user = msg.author
        self.question = question

    async def bool_dialogue(self):
        """
        Creates an interactive bool dialogue message for a user to react to.
        :return:
        :rtype: DialogueResponse
        """
        response = DialogueResponse(self)
        ongoing = Ongoing.is_ongoing('dialogue', self.msg.author.id)
        if not ongoing:
            Ongoing.set_ongoing('dialogue', self.user.id)
            self.question.set_author(name=self.user.display_name, icon_url=user_avatar(self.user))
            # noinspection PyBroadException
            try:
                confirmation = await self.channel.send(embed=self.question)
                [await confirmation.add_reaction(preac) for preac in BOOL_REACTIONS]
            except Exception:
                Ongoing.del_ongoing('dialogue', self.user.id)
                response.error = True
                return response

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
                same_author = usr.id == self.user.id
                same_message = reac.message.id == confirmation.id
                valid_reaction = str(reac.emoji) in BOOL_REACTIONS
                return same_author and same_message and valid_reaction

            try:
                ae, au = await self.bot.wait_for('reaction_add', timeout=TIMEOUT, check=check_emote)
                if ae.emoji == CONFIRM_REACT:
                    response.ok = True
                else:
                    response.cancelled = True
            except asyncio.TimeoutError:
                response.timed_out = True
            try:
                await confirmation.delete()
            except discord.NotFound:
                pass
            Ongoing.del_ongoing('dialogue', self.user.id)
        else:
            response.ongoing = True
        return response

    async def int_dialogue(self, start, end):
        """
        Creates an interactive int dialogue message for a user to react to.
        :param start: The number to start the range at.
        :type start: int
        :param end: The number to end the range at.
        :type end: int
        :return:
        :rtype: DialogueResponse
        """
        response = DialogueResponse(self)
        ongoing = Ongoing.is_ongoing('dialogue', self.user.id)
        if not ongoing:
            Ongoing.set_ongoing('dialogue', self.user.id)
            start = 0 if start < 0 else start
            end = 9 if end > 9 else end
            self.question.set_author(name=self.user.display_name, icon_url=user_avatar(self.user))
            # noinspection PyBroadException
            try:
                confirmation = await self.channel.send(embed=self.question)
                [await confirmation.add_reaction(INT_REACTIONS[preac]) for preac in range(start, end + 1)]
                await confirmation.add_reaction(CANCEL_REACT)
            except Exception:
                response.error = True
                Ongoing.del_ongoing('dialogue', self.user.id)
                return response

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
                same_author = usr.id == self.user.id
                same_message = reac.message.id == confirmation.id
                valid_reaction = (str(reac.emoji) in INT_REACTIONS) or str(reac.emoji) == CANCEL_REACT
                return same_author and same_message and valid_reaction

            try:
                ae, au = await self.bot.wait_for('reaction_add', timeout=TIMEOUT, check=check_emote)
                if str(ae.emoji) == CANCEL_REACT:
                    response.cancelled = True
                else:
                    response.ok = True
                    for react_index, int_react in enumerate(INT_REACTIONS):
                        if int_react == str(ae.emoji):
                            response.value = react_index
                            break
            except asyncio.TimeoutError:
                response.timed_out = True
            try:
                await confirmation.delete()
            except discord.NotFound:
                pass
            Ongoing.del_ongoing('dialogue', self.user.id)
        else:
            response.ongoing = True
        return response

    async def item_dialogue(self, icons, item):
        """
        Creates an interactive item dialogue message for a user to react to.
        :param icons: The icons to display on the message.
        :type icons: dict
        :param item: The item to base the item dialogue on.
        :type item: sigma.modules.minigames.professions.nodes.item_object.SigmaRawItem
        :return:
        :rtype: DialogueResponse
        """
        response = DialogueResponse(self)
        ongoing = Ongoing.is_ongoing('dialogue', self.user.id)
        if not ongoing:
            Ongoing.set_ongoing('dialogue', self.user.id)
            icon_list = [icons.get(ic) for ic in icons if icons.get(ic) != item.icon]
            icon_list.pop(0)
            possible_proto = [item.icon]
            while len(possible_proto) < secrets.randbelow(2) + 3:
                possible_proto.append(icon_list.pop(secrets.randbelow(len(icon_list))))
            possible = []
            while possible_proto:
                possible.append(possible_proto.pop(secrets.randbelow(len(possible_proto))))
            possible.append(CANCEL_REACT)
            title = f'{item.icon} Quick! Get the correct {item.type.lower()}!'
            self.question = discord.Embed(color=item.color, title=title)
            self.question.set_author(name=self.user.display_name, icon_url=user_avatar(self.user))
            # noinspection PyBroadException
            try:
                confirmation = await self.channel.send(embed=self.question)
                [await confirmation.add_reaction(preac) for preac in possible]
            except Exception:
                response.error = True
                Ongoing.del_ongoing('dialogue', self.user.id)
                return response

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
                same_author = usr.id == self.user.id
                same_message = reac.message.id == confirmation.id
                valid_reaction = str(reac.emoji) in possible
                return same_author and same_message and valid_reaction

            try:
                ae, au = await self.bot.wait_for('reaction_add', timeout=TIMEOUT, check=check_emote)
                if ae.emoji == item.icon:
                    response.ok = True
                elif str(ae.emoji) == CANCEL_REACT:
                    response.cancelled = True
                else:
                    response.cancelled = True
            except asyncio.TimeoutError:
                response.timed_out = True
            try:
                await confirmation.delete()
            except discord.NotFound:
                pass
            Ongoing.del_ongoing('dialogue', self.user.id)
        else:
            response.ongoing = True
        return response
