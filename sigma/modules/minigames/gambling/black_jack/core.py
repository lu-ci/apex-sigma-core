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
        self.deck = self.make_deck()
        self.dealer_hand = self.make_hand()
        self.player_hand = self.make_hand()

    @staticmethod
    def make_deck():
        deck = CARDS * 4
        decks = deck * 6
        shuffled = []
        while decks:
            card = decks.pop(secrets.randbelow(len(decks)))
            shuffled.append(card)
        return shuffled

    def make_hand(self):
        card_a = self.deck.pop(secrets.randbelow(len(self.deck)))
        card_b = self.deck.pop(secrets.randbelow(len(self.deck)))
        return [card_a, card_b]

    @staticmethod
    def get_hand_value(hand, dealer=False):
        hand_value = 0
        non_aces = list(filter(lambda x: x != 'Ace', hand))
        for card in non_aces:
            if card.isdigit():
                hand_value += int(card)
            else:
                hand_value += 10
        aces = list(filter(lambda x: x == 'Ace', hand))
        while aces:
            if dealer and hand_value + (11 * len(aces)) == 17:
                aces.pop(0)
                hand_value += 1
            elif hand_value + (11 * len(aces)) > 21:
                aces.pop(0)
                hand_value += 1
            else:
                hand_value += (11 * len(aces))
                break
        return hand_value

    async def dealer_hit(self, game_msg):
        while self.get_hand_value(self.dealer_hand, True) < 17:
            card = self.deck.pop(secrets.randbelow(len(self.deck)))
            self.dealer_hand.append(card)
        return await send_game_msg(self.channel, game_msg, self.generate_embed(False))

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

    def generate_embed(self, player_turn=True):
        embed = discord.Embed(color=0xDE2A42)
        embed.set_author(name=self.author.name, icon_url=user_avatar(self.author))
        if player_turn:
            dealer_str = f'Face Down, {self.dealer_hand[-1]}'
        else:
            dealer_str = ", ".join(self.dealer_hand)
        embed.description = f'**Dealer\'s Hand:** {dealer_str}\n'
        embed.description += f'**Your Hand:** {", ".join(self.player_hand)}'
        embed.set_footer(text='Emotes are hit, stand, double down.')
        return embed

    async def add_card(self, game_msg):
        card = self.deck.pop(secrets.randbelow(len(self.deck)))
        self.player_hand.append(card)
        return await send_game_msg(self.channel, game_msg, self.generate_embed())


async def send_game_msg(channel, game_msg, game_resp):
    """
    Edits the game message or resends if it an edit is not possible.
    :type channel: discord.TextChannel
    :type game_msg: discord.Message
    :type game_resp: discord.Embed
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
    :type bot: sigma.core.sigma.ApexSigma
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
    base_cooldown = 60
    cooldown = int(base_cooldown - ((base_cooldown / 100) * ((0 * 0.5) / (1.25 + (0.01 * 0)))))
    if cooldown < 12:
        cooldown = 12
    await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, cooldown)
