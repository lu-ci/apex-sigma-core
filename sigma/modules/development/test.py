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

import asyncio

import discord

from sigma.core.mechanics.command import SigmaCommand


async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    lcg = discord.utils.find(lambda g: g.id == 200751504175398912, cmd.bot.guilds)
    profiles = await cmd.db[cmd.db.db_nam].Profiles.find().to_list(None)
    total_chev = 0
    total_curr = 0
    total_usrs = 0
    currency = cmd.bot.cfg.pref.currency
    cicon = cmd.bot.cfg.pref.currency_icon
    started = discord.Embed(color=0xaa8dd8, title=f'{cicon} Started converting chevrons into {currency}...')
    await message.channel.send(embed=started)
    for profile in profiles:
        uid = profile.get('user_id')
        user = discord.utils.find(lambda u: u.id == uid, cmd.bot.get_all_members())
        if user:
            chevs = profile.get('chevrons', {}).get('total', 0)
            if chevs:
                total_chev += chevs
                chev_mult = chevs * 0.022222
                award = int(chevs * (22222 * (0.977777 + chev_mult)))
                total_curr += award
                await cmd.db.add_currency(user, lcg, award, False)
                cmd.log.info(f'{uid} gets {award} ')
                total_usrs += 1
                to_usr = discord.Embed(color=0xaa8dd8, title=f'{cicon} Your {chevs} turned into {award} {currency}.')
                try:
                    await user.send(embed=to_usr)
                    await asyncio.sleep(1)
                except Exception:
                    pass
        profile.pop('_id')
        if 'chevrons' in profile:
            profile.pop('chevrons')
        await cmd.db[cmd.db.db_nam].Profiles.update_one({'user_id': uid}, {'$set': profile})
    tally = f'{cicon} {total_curr} {currency} from {chevs} chevrons to {total_usrs} users.'
    response = discord.Embed(color=0xaa8dd8, title=tally)
    await message.channel.send(embed=response)

