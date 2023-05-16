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

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.gambling.black_jack.core import BlackJack, send_game_msg, set_blackjack_cd
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing

GAME_EMOTES = ['🔵', '🔴', '⏫']
BJ_RATIO = 6 / 5


async def blackjack(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        if not Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
            bet = 10
            if pld.args:
                if pld.args[0].isdigit():
                    bet = abs(int(pld.args[0]))
            currency_icon = cmd.bot.cfg.pref.currency_icon
            currency = cmd.bot.cfg.pref.currency
            author = pld.msg.author.id
            current_kud = await cmd.db.get_resource(author, 'currency')
            current_kud = current_kud.current
            if current_kud >= bet:
                Ongoing.set_ongoing(cmd.name, pld.msg.channel.id)
                await set_blackjack_cd(cmd, pld)

                bljk = BlackJack(pld.msg)
                if bljk.check_blackjack():
                    if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
                        Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
                    await cmd.db.add_resource(author, 'currency', bet * BJ_RATIO, cmd.name, pld.msg, False)
                    title = f'🎉 You got a BlackJack and won {int(bet * BJ_RATIO)} {currency}!'
                    bj_embed = discord.Embed(color=0xDE2A42, title=title)
                    bj_embed.set_footer(text=f'You won {int(100 * BJ_RATIO)}% of your original bet.')
                    await pld.msg.channel.send(embed=bj_embed)
                    return

                game_embed = bljk.generate_embed()
                game_msg = await pld.msg.channel.send(embed=game_embed)
                [await game_msg.add_reaction(e) for e in GAME_EMOTES]

                def check_emote(react):
                    """
                    Checks for a valid message reaction.
                    :type reac: discord.RawReactionActionEvent
                    :rtype: bool
                    """
                    same_author = react.user_id == pld.msg.author.id
                    same_message = react.message_id == game_msg.id
                    valid_reaction = str(react.emoji) in GAME_EMOTES
                    return same_author and same_message and valid_reaction

                finished, bust, win = False, False, False
                while not finished and not bust and not win:
                    try:
                        ae = await cmd.bot.wait_for('raw_reaction_add', timeout=60, check=check_emote)
                        # noinspection PyBroadException
                        try:
                            await game_msg.remove_reaction(ae.emoji, pld.msg.author)
                        except Exception:
                            pass
                        if str(ae.emoji) == '🔵':
                            game_msg = await bljk.add_card(game_msg)
                            finished = bljk.check_bust()
                        elif str(ae.emoji) == '🔴':
                            finished = True
                        elif str(ae.emoji) == '⏫':
                            if len(bljk.player_hand) == 2:
                                if current_kud >= bet * 2:
                                    bet += bet
                                    game_msg = await bljk.add_card(game_msg)
                                    finished = True
                                else:
                                    embed = bljk.generate_embed()
                                    embed.set_footer(text=f'Insufficient {currency} to double down.')
                                    game_msg = await send_game_msg(pld.msg.channel, game_msg, embed)
                            else:
                                embed = bljk.generate_embed()
                                embed.set_footer(text='You can only double down on your first turn.')
                                game_msg = await send_game_msg(pld.msg.channel, game_msg, embed)
                    except asyncio.TimeoutError:
                        if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
                            Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
                        await cmd.db.del_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg)
                        timeout_title = f'🕙 Time\'s up {pld.msg.author.display_name}!'
                        timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                        timeout_embed.set_footer(text=f'You lost {bet} {currency}.')
                        await pld.msg.channel.send(embed=timeout_embed)
                        return
                await bljk.dealer_hit(game_msg)
                if bljk.check_bust():
                    await cmd.db.del_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg)
                    title = f'💣 Your hand bust and you lost {bet} {currency}.'
                    response = discord.Embed(color=0x232323, title=title)
                elif bljk.check_dealer_bust():
                    await cmd.db.add_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg, False)
                    title = f'{currency_icon} The dealer bust and you won {bet} {currency}!'
                    response = discord.Embed(color=0x66cc66, title=title)
                elif bljk.check_push():
                    title = '🔵 You pushed and broke even.'
                    response = discord.Embed(color=0x3B88C3, title=title)
                elif bljk.check_win():
                    await cmd.db.add_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg, False)
                    title = f'{currency_icon} You beat the dealer and won {bet} {currency}!'
                    response = discord.Embed(color=0x66cc66, title=title)
                else:
                    await cmd.db.del_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg)
                    title = f'💣 The dealer won and you lost {bet} {currency}.'
                    response = discord.Embed(color=0x232323, title=title)
                if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
                    Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
            else:
                response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have {bet} {currency}.')
        else:
            response = GenericResponse('There is already one ongoing.').error()
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You can play again in {timeout} seconds.')
    await pld.msg.channel.send(embed=response)
