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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload

deck_cache = {}

suits = {'♥': 'Hearts', '♠': 'Spades', '♦': 'Diamonds', '♣': 'Clubs'}
names = {1: 'Ace', 12: 'Jack', 13: 'Queen', 14: 'King'}


def make_new_deck(uid):
    card_list = []
    for suit in list(suits):
        for val in range(1, 15):
            if val != 11:
                card = (suit, val)
                card_list.append(card)
    deck_cache.update({uid: card_list})
    return deck_cache.get(uid)


async def drawcard(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        try:
            amount = int(args[0])
            if amount > 10:
                amount = 10
            if amount < 1:
                amount = 1
        except ValueError:
            amount = 1
    else:
        amount = 1
    deck = deck_cache.get(message.author.id) or make_new_deck(message.author.id)
    if not len(deck) < amount:
        card_list = []
        while len(card_list) < amount:
            deck_count = len(deck)
            card = deck.pop(secrets.randbelow(deck_count))
            card_list.append(card)
        card_lines = []
        resp_clr = secrets.choice([0xdd2e44, 0x292f33])
        resp_icon = secrets.choice(list(suits))
        end = '' if len(card_list) == 1 else 's'
        resp_title = f'You drew {amount} card{end}...'
        for card in card_list:
            card_name = names.get(card[1]) or card[1]
            card_suit = suits.get(card[0]) or card[0]
            card_lines.append(f'{card[0]} **{card_name}** of **{card_suit}**')
        response = discord.Embed(color=resp_clr, title=f'{resp_icon} {resp_title}')
        response.description = '\n'.join(card_lines)
    else:
        prefix = await cmd.db.get_prefix(message)
        no_cards_title = f'❗ Your deck only has {len(deck)} cards, please use the {prefix}newdeck command.'
        response = discord.Embed(color=0xBE1931, title=no_cards_title)
    await message.channel.send(embed=response)
