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


async def declinesuggestion(cmd: SigmaCommand, message: discord.Message, args: list):
    if len(args) >= 2:
        token = args[0].lower()
        reason = ' '.join(args[1:])
        suggestion = await cmd.db[cmd.db.db_nam].Suggestions.find_one({'suggestion.id': token})
        if suggestion:
            athr = discord.utils.find(lambda u: u.id == suggestion.get('user', {}).get('id'), cmd.bot.get_all_members())
            if athr:
                to_user_title = f'⛔ Suggestion {token} declined by {message.author.display_name}.'
                to_user = discord.Embed(color=0xBE1931, title=to_user_title)
                to_user.description = reason
                try:
                    await athr.send(embed=to_user)
                    response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {token} declined.')
                except (discord.Forbidden, discord.NotFound):
                    response = discord.Embed(color=0xBE1931, title='❗ Failed to send the notification.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The author wasn\'t found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No suggestion entry with that ID was found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    await message.channel.send(embed=response)
