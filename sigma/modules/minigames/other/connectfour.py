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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.other.connect_four.core import ConnectFourBoard
from sigma.modules.minigames.utils.ongoing.ongoing import del_ongoing, is_ongoing, set_ongoing

nums = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']


def generate_response(avatar, current, rows):
    """
    :param avatar:
    :type avatar: str
    :param current:
    :type current: discord.Member
    :param rows:
    :type rows: list[list[str]]
    :return:
    :rtype: discord.Embed
    """
    board_out = "\n".join([' '.join(row) for row in rows])
    board_resp = discord.Embed(color=0x2156be, description=board_out)
    board_resp.set_author(icon_url=avatar, name='Connect Four')
    board_resp.set_footer(text=f'{current.display_name}\'s Turn.')
    return board_resp


async def send_board_msg(message, board_msg, board_resp):
    """
    :param message:
    :type message: discord.Message
    :param board_msg:
    :type board_msg: discord.Message
    :param board_resp:
    :type board_resp: discord.Embed
    :return:
    :rtype: discord.Message
    """
    replaced = False
    if board_msg:
        try:
            await board_msg.edit(embed=board_resp)
        except discord.NotFound:
            board_msg = await message.channel.send(embed=board_resp)
            replaced = True
    else:
        board_msg = await message.channel.send(embed=board_resp)
        replaced = True
    if replaced:
        [await board_msg.add_reaction(num) for num in nums]
    return board_msg


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
        if reaction.emoji in nums:
            present_emotes.append(reaction.emoji)
        async for emote_author in reaction.users():
            if emote_author.id != bid:
                await msg.remove_reaction(reaction.emoji, emote_author)
    for num in nums:
        if num not in present_emotes:
            await msg.add_reaction(num)


async def connectfour(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not is_ongoing(cmd.name, pld.msg.channel.id):
        set_ongoing(cmd.name, pld.msg.channel.id)
        competitor, curr_turn = None, pld.msg.author
        color = pld.args[0][0].lower() if pld.args else None
        player, bot = ('b', 'r') if color == 'b' else ('r', 'b')
        if pld.msg.mentions:
            if pld.msg.mentions[0].id != pld.msg.author.id and not pld.msg.mentions[0].bot:
                competitor = bot
                bot = None
            else:
                ender = 'another bot' if pld.msg.mentions[0].bot else 'yourself'
                self_embed = error(f'You can\'t play against {ender}.')
                await pld.msg.channel.send(embed=self_embed)
                return

        board = ConnectFourBoard()
        user_av = user_avatar(pld.msg.author)
        board_resp = generate_response(user_av, pld.msg.author, board.make)
        board_msg = await pld.msg.channel.send(embed=board_resp)
        [await board_msg.add_reaction(num) for num in nums]

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
            same_author = usr.id == pld.msg.author.id
            same_message = reac.message.id == board_msg.id
            valid_reaction = str(reac.emoji) in nums
            return same_author and same_message and valid_reaction

        finished, winner, win = False, None, False
        last_bot_move = 3
        while not finished:
            try:
                ae, au = await cmd.bot.wait_for('reaction_add', check=check_emote, timeout=30)
                await check_emotes(cmd.bot, ae.message)
                piece = player if curr_turn.id == pld.msg.author.id else competitor
                opponent = pld.msg.guild.me if bot else pld.msg.mentions[0]
                next_player = pld.msg.author if curr_turn != pld.msg.author else opponent
                board_resp = generate_response(user_av, next_player, board.edit(nums.index(str(ae.emoji)), piece))
                board_msg = await send_board_msg(pld.msg, board_msg, board_resp)
                full, winner, win = board.winner
                finished = win or full
                if not finished:
                    if not competitor:
                        # Bot takes turn
                        await asyncio.sleep(2)
                        last_bot_move = bot_choice = board.bot_move(last_bot_move)
                        board_resp = generate_response(user_av, pld.msg.author, board.edit(bot_choice, bot))
                        board_msg = await send_board_msg(pld.msg, board_msg, board_resp)
                        full, winner, win = board.winner
                        finished = win or full
                    else:
                        if curr_turn == pld.msg.author:
                            curr_turn = pld.msg.mentions[0]
                        else:
                            curr_turn = pld.msg.author

            except asyncio.TimeoutError:
                timeout_title = f'🕙 Time\'s up {curr_turn.display_name}!'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await pld.msg.channel.send(embed=timeout_embed)
                if is_ongoing(cmd.name, pld.msg.channel.id):
                    del_ongoing(cmd.name, pld.msg.channel.id)
                return

        if winner:
            if bot:
                if winner == getattr(board, player):
                    color, icon, resp = 0x3B88C3, '💎', 'You win'
                else:
                    color, icon, resp = 0x292929, '💣', 'You lose'
            else:
                color, icon, resp = 0x3B88C3, '💎', f'{curr_turn.display_name} wins'
        else:
            color, icon, resp = 0xFFCC4D, '🔥', 'It\'s a draw'
        response = discord.Embed(color=color, title=f'{icon} {resp}!')
        await pld.msg.channel.send(embed=response)
        if is_ongoing(cmd.name, pld.msg.channel.id):
            del_ongoing(cmd.name, pld.msg.channel.id)
    else:
        ongoing_error = error('There is already one ongoing.')
        await pld.msg.channel.send(embed=ongoing_error)
