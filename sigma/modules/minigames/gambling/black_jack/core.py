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

import secrets

import discord

from sigma.core.utilities.data_processing import user_avatar

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
GAME_EMOTES = ['🔵', '🔴', '⏫']


class BlackJack(object):
    def __init__(self, message):
        self.author = message.author
        self.channel = message.channel
        self.deck = CARDS * 4
        self.dealer_hand = self.make_hand()
        self.player_hand = self.make_hand()

    def make_hand(self):
        card_a = self.deck.pop(secrets.randbelow(len(self.deck)))
        card_b = self.deck.pop(secrets.randbelow(len(self.deck)))
        return [card_a, card_b]

    @staticmethod
    def get_hand_value(hand, dealer=False):
        hand_value = 0
        sorted_hand = sorted(hand, key=lambda x: x != 'Ace', reverse=True)
        for card in sorted_hand:
            if card.isdigit():
                hand_value += int(card)
            elif card == 'Ace':
                if hand_value + 11 > 21:
                    hand_value += 1
                else:
                    if dealer:
                        if hand_value + 11 == 17:
                            hand_value += 1
                        else:
                            hand_value += 11
                    else:
                        hand_value += 11
            else:
                hand_value += 10
        return hand_value

    async def dealer_hit(self, game_msg):
        while self.get_hand_value(self.dealer_hand) < 17:
            card = self.deck.pop(secrets.randbelow(len(self.deck)))
            self.dealer_hand.append(card)
        return await send_game_msg(self.channel, game_msg, self.generate_embed())

    def check_dealer_bust(self):
        return self.get_hand_value(self.dealer_hand) > 21

    def check_bust(self):
        return self.get_hand_value(self.player_hand) > 21

    def check_push(self):
        player_hand_value = self.get_hand_value(self.player_hand)
        dealer_hand_value = self.get_hand_value(self.dealer_hand)
        return dealer_hand_value == player_hand_value

    def check_win(self):
        player_hand_value = self.get_hand_value(self.player_hand)
        dealer_hand_value = self.get_hand_value(self.dealer_hand)
        return dealer_hand_value > 21 or player_hand_value > dealer_hand_value

    def check_blackjack(self):
        return self.get_hand_value(self.player_hand) == 21

    def generate_embed(self, start=False):
        embed = discord.Embed(color=0xDE2A42)
        embed.set_author(name=self.author.name, icon_url=user_avatar(self.author))
        if start:
            dealer_str = f'Face Down, {self.dealer_hand[-1]}'
        else:
            dealer_str = ", ".join(sorted(self.dealer_hand, reverse=True))
        embed.description = f'**Dealer\'s Hand:** {dealer_str}\n'
        embed.description += f'**Your Hand:** {", ".join(sorted(self.player_hand, reverse=True))}'
        embed.set_footer(text='Emotes are hit, stand, double down.')
        return embed

    async def add_card(self, game_msg):
        card = self.deck.pop(secrets.randbelow(len(self.deck)))
        self.player_hand.append(card)
        return await send_game_msg(self.channel, game_msg, self.generate_embed())


async def send_game_msg(channel, game_msg, game_resp):
    """
    Edits the game message or resends if it an edit is not possible.
    :param channel: The channel the message is in.
    :type channel: discord.TextChannel
    :param game_msg: The message to edit.
    :type game_msg: discord.Message
    :param game_resp: The embed to change to.
    :type game_resp: discord.Embed
    :return:
    :rtype: discord.Message
    """
    replaced = False
    if game_msg:
        try:
            await game_msg.edit(embed=game_resp)
        except discord.NotFound:
            game_msg = await channel.send(embed=game_resp)
            replaced = True
    else:
        game_msg = await channel.send(embed=game_resp)
        replaced = True
    if replaced:
        [await game_msg.add_reaction(emote) for emote in GAME_EMOTES]
    return game_msg


async def check_emotes(bot, msg):
    """
    Ensures only the correct reactions are present on the message.
    :param bot: The core client class.
    :type bot: sigma.core.sigma.ApexSigma
    :param msg: The message to process.
    :type msg: discord.Message
    """
    bid = bot.user.id
    present_emotes = []
    for reaction in msg.reactions:
        if reaction.emoji in GAME_EMOTES:
            present_emotes.append(reaction.emoji)
        async for emote_author in reaction.users():
            if emote_author.id != bid:
                await msg.remove_reaction(reaction.emoji, emote_author)
    for emote in GAME_EMOTES:
        if emote not in present_emotes:
            await msg.add_reaction(emote)


async def set_blackjack_cd(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
    base_cooldown = 60
    stamina = upgrade_file.get('casino', 0)
    cooldown = int(base_cooldown - ((base_cooldown / 100) * ((stamina * 0.5) / (1.25 + (0.01 * stamina)))))
    if cooldown < 12:
        cooldown = 12
    await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, cooldown)
