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


import discord

from sigma.core.mechanics.command import SigmaCommand


async def award(cmd: SigmaCommand, index: int, uid: int, gld: discord.Guild):
    mult = 20 - index
    aw_amt = 100000 * mult
    all_members = cmd.bot.get_all_members()
    member = discord.utils.find(lambda x: x.id == uid, all_members)
    if member:
        await cmd.db.add_currency(member, gld, aw_amt, False)


async def awardleaderboards(cmd: SigmaCommand, message: discord.Message, args: list):
    patterns = [['CurrencySystem', 'global'], ['ExperienceSystem', 'global'], ['Cookies', 'cookies']]
    for pattern in patterns:
        col_nam = pattern[0]
        val_fil = pattern[1]
        winners = await cmd.db[cmd.db.db_nam][col_nam].find({}).sort([(val_fil, -1)]).limit(20).to_list(None)
        position = 0
        for winner in winners:
            await award(cmd, position, winner.get('user_id'), message.guild)
            position += 1
    currency_icon = cmd.bot.cfg.pref.currency_icon
    response = discord.Embed(color=0xaa8dd8, title=f'{currency_icon} All members have been awarded.')
    await message.channel.send(embed=response)
