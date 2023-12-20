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

from sigma.core.utilities.generic_responses import GenericResponse


def count_votes(poll_file):
    """
    :type poll_file: dict
    :rtype: dict
    """
    vote_coll = {}
    for vote in poll_file['votes'].keys():
        vote_index = poll_file['votes'].get(vote)
        if vote_index in vote_coll:
            curr = vote_coll.get(vote_index)
        else:
            curr = 0
        curr += 1
        vote_coll.update({vote_index: curr})
    return vote_coll


def make_bar(points, total):
    """
    :type points: int
    :type total: int
    :rtype: str
    """
    try:
        fill = int((points / total) * 10)
    except ZeroDivisionError:
        fill = 0
    empty = 10 - fill
    bar = f'[{fill * "▣"}{empty * "▢"}]'
    return bar


async def shadowpollstats(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        poll_id = pld.args[0].lower()
        poll_file = await cmd.db[cmd.db.db_name].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            visible = poll_file['settings']['visible']
            if author == pld.msg.author.id or visible:
                total = len(list(poll_file['votes']))
                vote_coll = count_votes(poll_file)
                loop_index = 0
                output = f'Total Votes: {total}'
                for option in poll_file['poll']['answers']:
                    loop_index += 1
                    if loop_index in vote_coll:
                        points = vote_coll.get(loop_index)
                    else:
                        points = 0
                    if len(option) > 10:
                        option = option[:7] + '...'
                    bar = make_bar(points, total)
                    try:
                        perc_base = points / total
                    except ZeroDivisionError:
                        perc_base = 0
                    stat_line = f'[{points}] {bar} {int(perc_base * 100)}% - {option}'
                    output += f'\n{stat_line}'
                response = discord.Embed(color=0xF9F9F9, title=f'📊 Poll {poll_id} Statistics.')
                response.description = f'```\n{output}\n```'
            else:
                response = discord.Embed(color=0xFFCC4D, title='🔒 You can\'t view this poll\'s stats.')
        else:
            response = GenericResponse('Poll not found.').not_found()
    else:
        response = GenericResponse('Missing poll ID.').error()
    await pld.msg.channel.send(embed=response)
