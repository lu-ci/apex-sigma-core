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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.other.connect_four.connect_four_mechanics import make_game
from sigma.modules.minigames.other.connect_four.core import ConnectFourBoard
from sigma.modules.minigames.utils.ongoing.ongoing import is_ongoing, set_ongoing

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


async def connectfour(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not is_ongoing(cmd.name, pld.msg.channel.id):
        color = pld.args[0][0].lower() if pld.args else None
        competitor = pld.msg.guild.me
        if pld.msg.mentions:
            is_author = pld.msg.mentions[0].id == pld.msg.author.id
            is_me = pld.msg.mentions[0].id == cmd.bot.user.id
            is_bot = pld.msg.mentions[0].bot
            if not is_author and not is_bot or is_me:
                competitor = pld.msg.mentions[0]
            else:
                ender = 'another bot' if pld.msg.mentions[0].bot else 'yourself'
                self_embed = error(f'You can\'t play against {ender}.')
                await pld.msg.channel.send(embed=self_embed)
                return

        set_ongoing(cmd.name, pld.msg.channel.id)
        board = ConnectFourBoard()
        user_av = user_avatar(pld.msg.author)
        board_resp = generate_response(user_av, pld.msg.author, board.make)
        board_msg = await pld.msg.channel.send(embed=board_resp)
        [await board_msg.add_reaction(num) for num in nums]
        await make_game(board_msg, board, pld.msg.author, competitor, color)
    else:
        ongoing_error = error('There is already one ongoing.')
        await pld.msg.channel.send(embed=ongoing_error)
