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

import arrow
import discord

from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.other.connect_four.core import ConnectFourGame
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

cf_cache = MemoryCacher(CacheConfig({}))
nums = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']


async def make_game(message, board, p_one, p_two, color):
    """
    :type message: discord.Message
    :type board: sigma.modules.minigames.other.connect_four.core.ConnectFourBoard
    :type p_one: discord.Member
    :type p_two: discord.Member
    :type color: str
    """
    po_piece, pt_piece = ('b', 'r') if color == 'b' else ('r', 'b')
    data = {
        'board': board,
        'p_one': p_one,
        'p_two': p_two,
        'po_piece': po_piece,
        'pt_piece': pt_piece,
        'current_turn': p_one,
        'last_bot_move': 3,
        'is_bot': p_two.bot,
        'expiry': arrow.utcnow().int_timestamp + 120,
        'channel_id': message.channel.id
    }
    await cf_cache.set_cache(message.id, ConnectFourGame(data))


def generate_response(avatar, current, rows):
    """
    :type avatar: str
    :type current: discord.Member
    :type rows: list[list[str]]
    :rtype: discord.Embed
    """
    board_out = "\n".join([' '.join(row) for row in rows])
    board_resp = discord.Embed(color=0x2156be, description=board_out)
    board_resp.set_author(icon_url=avatar, name='Connect Four')
    board_resp.set_footer(text=f'{current.display_name}\'s Turn.')
    return board_resp


async def send_board_msg(channel, board_msg, board_resp):
    """
    :type channel: discord.TextChannel
    :type board_msg: discord.Message
    :type board_resp: discord.Embed
    :rtype: discord.Message
    """
    replaced = False
    if board_msg:
        try:
            await board_msg.edit(embed=board_resp)
        except discord.NotFound:
            board_msg = await channel.send(embed=board_resp)
            replaced = True
    else:
        board_msg = await channel.send(embed=board_resp)
        replaced = True
    if replaced:
        [await board_msg.add_reaction(num) for num in nums]
    return board_msg


async def check_emotes(bot, msg):
    """

    Ensures only the correct reactions are present on the message.
    :type bot: sigma.core.sigma.ApexSigma
    :type msg: discord.Message
    """
    bid = bot.user.id
    present_emotes = []
    for reaction in msg.reactions:
        if reaction.emoji in nums:
            present_emotes.append(reaction.emoji)
        async for emote_author in reaction.users():
            if emote_author.id != bid:
                await msg.remove_reaction(reaction.emoji, emote_author)
    for num in nums:
        if num not in present_emotes:
            await msg.add_reaction(num)


async def connect_four_mechanics(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.RawReactionPayload
    """
    payload = pld.raw
    uid = payload.user_id
    cid = payload.channel_id
    mid = payload.message_id
    emoji = payload.emoji
    channel = await ev.bot.get_channel(cid)
    try:
        guild = channel.guild
    except AttributeError:
        guild = None
    if guild:
        # noinspection PyTypeChecker
        game: ConnectFourGame = await cf_cache.get_cache(mid)
        if game:
            if Ongoing.is_ongoing('cf_ongoing_turn', cid):
                return
            Ongoing.set_ongoing('cf_ongoing_turn', cid)
            try:
                message = await channel.fetch_message(mid)
            except (discord.NotFound, discord.Forbidden):
                message = None
            if message:
                if ev.event_type == 'raw_reaction_add':
                    if str(emoji.name) in nums and uid == game.current_turn.id:
                        user_av = user_avatar(game.p_one)
                        await check_emotes(ev.bot, message)
                        piece = game.po_piece if game.current_turn.id == game.p_one.id else game.pt_piece
                        opponent = message.guild.me if game.is_bot else game.p_two
                        next_player = game.p_one if game.current_turn != game.p_one else opponent
                        rows = game.board.edit(nums.index(str(emoji.name)), piece)
                        board_resp = generate_response(user_av, next_player, rows)
                        board_msg = await send_board_msg(channel, message, board_resp)
                        full, winner, win = game.board.winner
                        finished = win or full
                        if not finished:
                            if game.is_bot:
                                # Bot takes turn
                                await asyncio.sleep(2)
                                game.last_bot_move = bot_choice = game.board.bot_move(game.last_bot_move)
                                rows = game.board.edit(bot_choice, game.pt_piece)
                                board_resp = generate_response(user_av, game.p_one, rows)
                                await send_board_msg(channel, board_msg, board_resp)
                                full, winner, win = game.board.winner
                                finished = win or full
                            else:
                                if game.current_turn == game.p_one:
                                    game.current_turn = game.p_two
                                else:
                                    game.current_turn = game.p_one
                        if finished:
                            if winner:
                                if game.is_bot:
                                    if winner == getattr(game.board, piece):
                                        color, icon, resp = 0x3B88C3, '💎', 'You win'
                                    else:
                                        color, icon, resp = 0x292929, '💣', 'You lose'
                                else:
                                    color, icon, resp = 0x3B88C3, '💎', f'{game.current_turn.display_name} wins'
                            else:
                                color, icon, resp = 0xFFCC4D, '🔥', 'It\'s a draw'
                            response = discord.Embed(color=color, title=f'{icon} {resp}!')
                            await channel.send(embed=response)
                            await cf_cache.del_cache(mid)
                            if Ongoing.is_ongoing('connectfour', channel.id):
                                Ongoing.del_ongoing('connectfour', channel.id)
            game.expiry = arrow.utcnow().int_timestamp + 120
            if Ongoing.is_ongoing('cf_ongoing_turn', cid):
                Ongoing.del_ongoing('cf_ongoing_turn', cid)
