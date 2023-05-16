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
from sigma.core.utilities.generic_responses import GenericResponse

hor_1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
hor_2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
hor_3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

range_map = {
    'number': range(0, 37),
    'type': ['odd', 'even'],
    'color': ['red', 'black'],
    'column': range(1, 4),
    'dozen': range(1, 4),
    'half': [1, 2]
}

multi_map = {
    'number': 35,
    'type': 1,
    'color': 1,
    'column': 2,
    'dozen': 2,
    'half': 1
}


class RouletteSpot(object):
    def __init__(self, number):
        self.number = number
        self.type = 'odd' if divmod(number, 2)[1] else 'even'
        self.color = None if number == 0 else 'black' if divmod(number, 2)[1] else 'red'
        self.color_icon = '🔵' if number == 0 else '⚫' if divmod(number, 2)[1] else '🔴'
        self.column = 3 if number in hor_3 else 2 if number in hor_2 else 1 if number in hor_1 else 0
        self.dozen = 3 if number >= 25 else 2 if number >= 13 else 1 if number >= 1 else 0
        self.half = 2 if number >= 19 else 1 if number >= 1 else 0
        self.desc = f'{self.color_icon} {self.number}: Column: {self.column} | Dozen: {self.dozen} | Half: {self.half}'


spots = [RouletteSpot(num) for num in range(0, 37)]


def get_bet(args):
    """
    :type args: list[str]
    :rtype: int
    """
    try:
        bet = abs(int(args[0]))
    except ValueError:
        bet = 10
    return bet


def get_selector_and_value(args):
    """
    :type args: list[str]
    :rtype:str, str
    """
    selector_split = [a.strip() for a in args[-1].split(':')]
    if len(selector_split) == 2:
        sel, val = [piece.strip().lower() for piece in selector_split]
        for key in range_map:
            if key.startswith(sel):
                sel = key
                break
        try:
            val = abs(int(val))
        except ValueError:
            pass
    else:
        sel = val = None
    return sel, val


async def set_roul_cd(cmd, pld):
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


async def roulette(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        if pld.args:
            sel, val = get_selector_and_value(pld.args)
            sel = 'color' if sel == 'colour' else sel
            if sel is not None and val is not None:
                if sel in range_map:
                    if val in range_map.get(sel):
                        bet = get_bet(pld.args)
                        currency_icon = cmd.bot.cfg.pref.currency_icon
                        currency = cmd.bot.cfg.pref.currency
                        author = pld.msg.author.id
                        current_kud = await cmd.db.get_resource(author, 'currency')
                        current_kud = current_kud.current
                        if current_kud >= bet:
                            await set_roul_cd(cmd, pld)
                            await cmd.db.del_resource(pld.msg.author.id, 'currency', bet, cmd.name, pld.msg)
                            spot = secrets.choice(spots)
                            spot_sel_val = getattr(spot, sel, val)
                            if spot_sel_val == val:
                                winnings = bet + (bet * multi_map.get(sel))
                                await cmd.db.add_resource(author, 'currency', winnings, cmd.name, pld.msg, False)
                                footer = f'{currency_icon} You won {winnings - bet} {currency}'
                                resp_color = 0x66cc66
                            else:
                                resp_color = 0xBE1931
                                footer = f'You lost {bet} {currency}'
                            footer += f' for betting on the {sel}.'
                            response = discord.Embed(color=resp_color, title=spot.desc)
                            response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
                            response.set_footer(text=footer)
                        else:
                            response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have {bet} {currency}.')
                    else:
                        ranges = range_map.get(sel)
                        valids = f'{ranges[0]} - {ranges[-1]}'
                        response = GenericResponse(f'Invalid value for {sel}. Accepted are {valids}').error()
                else:
                    response = GenericResponse('Invalid selector, check the command description.').error()
            else:
                response = GenericResponse('Invalid selector and value syntax.').error()
        else:
            response = GenericResponse('Missing selector.').error()
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You can spin again in {timeout} seconds.')
    await pld.msg.channel.send(embed=response)
