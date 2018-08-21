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


async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    lcg = discord.utils.find(lambda g: g.id == 200751504175398912, cmd.bot.guilds)
    profiles = await cmd.db.aurora.Profiles.find().to_list(None)
    for profile in profiles:
        uid = profile.get('user_id')
        user = discord.utils.find(lambda u: u.id == uid, cmd.bot.get_all_members())
        if user:
            chevs = profile.get('chevrons', {}).get('total', 0)
            if chevs:
                chev_mult = chevs * 0.022222
                award = int(chevs * (22222 * (1 + chev_mult)))
                await cmd.db.add_currency(user, lcg, award, False)
                cmd.log.info(f'{user.name} gets {award} ')
        profile.pop('_id')
        profile.pop('chevrons')
        await cmd.db.aurora.Profiles.update_one({'user_id', uid}, {'$set': profile})

