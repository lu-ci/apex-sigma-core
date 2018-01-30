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


async def removereminder(cmd, message, args):
    if args:
        rem_id = args[0].lower()
        lookup_data = {'UserID': message.author.id, 'ReminderID': rem_id}
        reminder = await cmd.db[cmd.db.db_cfg.database].Reminders.find_one(lookup_data)
        if reminder:
            await cmd.db[cmd.db.db_cfg.database].Reminders.delete_one(lookup_data)
            response = discord.Embed(color=0x66CC66, title=f'✅ Reminder {rem_id} has been deleted.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Reminder `{rem_id}` not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No reminder ID inputted.')
    await message.channel.send(embed=response)
