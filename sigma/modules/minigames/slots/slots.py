# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
from sigma.core.utilities.data_processing import user_avatar

rarity_rewards = {
    '🍆': 5,
    '🍒': 5,
    '⚓': 10,
    '🏵': 10,
    '💖': 15,
    '🏮': 15,
    '🍥': 20,
    '💵': 20,
    '💳': 25,
    '🎁': 25,
    '🐬': 30,
    '🐦': 30,
    '🌟': 35,
    '🦊': 35,
    '🦋': 40,
    '🐍': 40,
    '🍬': 45,
    '💎': 45,
    '🔰': 50,
    '⚜': 50
}

symbols = []
for symbol in rarity_rewards:
    symbols.append(symbol)


async def slots(cmd: SigmaCommand, message: discord.Message, args: list):
    currency_icon = cmd.bot.cfg.pref.currency_icon
    currency = cmd.bot.cfg.pref.currency
    current_kud = await cmd.db.get_currency(message.author, message.guild)
    current_kud = current_kud['current']
    if args:
        try:
            bet = abs(int(args[0]))
        except ValueError:
            bet = 10
    else:
        bet = 10
    if current_kud >= bet:
        if not await cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
            upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': message.author.id})
            sabotage_file = await cmd.db[cmd.db.db_cfg.database].SabotagedUsers.find_one({'UserID': message.author.id})
            if upgrade_file is None:
                await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one({'UserID': message.author.id})
                upgrade_file = {}
            base_cooldown = 60
            if 'casino' in upgrade_file:
                stamina = upgrade_file['casino']
            else:
                stamina = 0
            cooldown = int(base_cooldown - ((base_cooldown / 100) * ((stamina * 0.5) / (1.25 + (0.01 * stamina)))))
            if cooldown < 12:
                cooldown = 12
            await cmd.bot.cool_down.set_cooldown(cmd.name, message.author, cooldown)
            await cmd.db.rmv_currency(message.author, bet)
            out_list = []
            for x in range(0, 3):
                temp_list = []
                init_symb = []
                for y in range(0, 3):
                    if not init_symb:
                        symbol_choice = secrets.choice(symbols)
                        init_symb.append(symbol_choice)
                    else:
                        if sabotage_file:
                            roll = 999999999
                        else:
                            roll = secrets.randbelow(bet + (bet // 2) + 10)
                        if roll == 0:
                            symbol_choice = secrets.choice(init_symb)
                        else:
                            temp_symb = []
                            for symbol_item in symbols:
                                temp_symb.append(symbol_item)
                            for init_symb_item in init_symb:
                                temp_symb.remove(init_symb_item)
                            symbol_choice = secrets.choice(temp_symb)
                            init_symb.append(symbol_choice)
                    temp_list.append(symbol_choice)
                out_list.append(temp_list)
            slot_lines = f'⏸{"".join(out_list[0])}⏸'
            slot_lines += f'\n▶{"".join(out_list[1])}◀'
            slot_lines += f'\n⏸{"".join(out_list[2])}⏸'
            combination = out_list[1]
            three_comb = bool(combination[0] == combination[1] == combination[2])
            two_comb_one = bool(combination[0] == combination[1])
            two_comb_two = bool(combination[0] == combination[2])
            two_comb_three = bool(combination[1] == combination[2])
            if three_comb:
                win = True
                announce = True
                winnings = int(bet * (rarity_rewards[combination[0]] * (bet // 2)))
            elif two_comb_one or two_comb_two or two_comb_three:
                if combination[0] == combination[1]:
                    win_comb = combination[0]
                elif combination[0] == combination[2]:
                    win_comb = combination[0]
                elif combination[1] == combination[2]:
                    win_comb = combination[1]
                else:
                    win_comb = None
                win = True
                announce = False
                winnings = int(bet * (rarity_rewards[win_comb] * (bet // 5)))
            else:
                win = False
                announce = False
                winnings = 0
            if win:
                color = 0x5dadec
                title = '💎 Congrats, you won!'
                footer = f'{currency_icon} {winnings} {currency} has been awarded.'
                await cmd.db.add_currency(message.author, message.guild, winnings, additive=False)
            else:
                color = 0x232323
                title = '💣 Oh my, you lost...'
                footer = f'{currency_icon} {bet} {currency} has been deducted.'
            if announce:
                if 'win_channel' in cmd.cfg:
                    win_ch_id = cmd.cfg['win_channel']
                    target_channel = discord.utils.find(lambda c: c.id == win_ch_id, cmd.bot.get_all_channels())
                    announce_embed = discord.Embed(color=0xf9f9f9, title=f'🎰 A user just got 3 {combination[0]}.')
                    announce_embed.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
                    announce_embed.set_footer(text=f'On: {message.guild.name}.', icon_url=message.guild.icon_url)
                    await target_channel.send(embed=announce_embed)
            response = discord.Embed(color=color)
            response.add_field(name=title, value=slot_lines)
            response.set_footer(text=footer)
        else:
            timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
            response = discord.Embed(color=0x696969, title=f'🕙 You can spin again in {timeout} seconds.')
    else:
        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
    await message.channel.send(embed=response)
