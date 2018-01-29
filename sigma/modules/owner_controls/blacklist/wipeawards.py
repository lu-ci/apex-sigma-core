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
import discord


async def wipeawards(cmd, message, args):
    if args:
        uid = args[0]
        try:
            uid = int(uid)
        except ValueError:
            uid = None
        if uid:
            lookup = {'UserID': uid}
            collections = ['CurrencySystem', 'Cookies', 'ExperienceSystem', 'Inventory']
            for collection in collections:
                await cmd.db[cmd.db.db_cfg.database][collection].delete_one(lookup)
            target = discord.utils.find(lambda x: x.id == uid, cmd.bot.get_all_members())
            if target:
                unam = f'{target.name}#{target.discriminator}'
            else:
                unam = str(uid)
            response = discord.Embed(color=0x696969, title=f'🗑 Wiped {unam}\'s property.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)
