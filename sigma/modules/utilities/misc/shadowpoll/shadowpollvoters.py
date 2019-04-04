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

import discord

from sigma.core.utilities.generic_responses import denied, error, not_found


async def shadowpollvoters(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        poll_id = pld.args[0].lower()
        poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == pld.msg.author.id:
                votes = poll_file['votes']
                if votes:
                    response = discord.Embed(color=0xF9F9F9, title=f'📨 Poll {poll_id} Voters')
                    voter_lines = []
                    for voter_id in poll_file['votes'].keys():
                        voter_id = int(voter_id)
                        voter = await cmd.bot.get_user(voter_id)
                        if voter:
                            voter_line = f'{voter.name}#{voter.discriminator}'
                        else:
                            voter_line = f'{voter_id}'
                        voter_lines.append(voter_line)
                    response.description = '\n'.join(voter_lines)
                else:
                    response = error('Nobody voted yet.')
            else:
                response = denied('You didn\'t make this poll.')
        else:
            response = not_found('Poll not found.')
    else:
        response = error('Missing poll ID.')
    await pld.msg.channel.send(embed=response)
