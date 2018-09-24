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


async def wipeawards(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        target_id = None
        if args[0].isdigit():
            target_id = int(args[0])
        if target_id:
            lookup = {'user_id': target_id}
            collections = ['CurrencySystem', 'Cookies', 'ExperienceSystem', 'Inventory', 'Upgrades']
            for collection in collections:
                await cmd.db[cmd.db.db_nam][collection].delete_one(lookup)
            all_members = cmd.bot.users
            target = discord.utils.find(lambda x: x.id == target_id, all_members)
            unam = f'{target.name}#{target.discriminator}' if target else str(target_id)
            response = discord.Embed(color=0x696969, title=f'🗑 Wiped {unam}\'s property.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing guild ID.')
    await message.channel.send(embed=response)
