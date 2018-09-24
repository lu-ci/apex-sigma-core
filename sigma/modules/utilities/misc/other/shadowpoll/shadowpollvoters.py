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


async def shadowpollvoters(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        poll_id = args[0].lower()
        poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                votes = poll_file['votes']
                if votes:
                    response = discord.Embed(color=0xF9F9F9, title=f'📨 Poll {poll_id} Voters')
                    voter_lines = []
                    members = cmd.bot.users
                    for voter_id in poll_file['votes'].keys():
                        voter_id = int(voter_id)
                        voter = discord.utils.find(lambda x: x.id == voter_id, members)
                        if voter:
                            voter_line = f'{voter.name}#{voter.discriminator}'
                        else:
                            voter_line = f'{voter_id}'
                        voter_lines.append(voter_line)
                    response.description = '\n'.join(voter_lines)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Nobody voted yet.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 Poll not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
