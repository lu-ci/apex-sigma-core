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

from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import not_found


async def commandstatistics(cmd: SigmaCommand, pld: CommandPayload):
    all_stats = await cmd.db[cmd.db.db_nam].CommandStats.find({}).to_list(None)
    all_stats = [asi for asi in all_stats if asi.get('command') in cmd.bot.modules.commands]
    stat_list = sorted(all_stats, key=lambda k: k.get('count'), reverse=True)
    stat_list, page = PaginatorCore.paginate(stat_list, pld.args[0] if pld.args else 1, 15)
    if stat_list:
        out_list = [[sli.get('command').upper(), str(sli.get('count', 0))] for sli in stat_list]
        out_table = boop(out_list, ['Command', 'Count'])
        response = f'📟 **Command Statistics**: Page {page}'
        response += f'\n```hs\n{out_table}\n```'
        await pld.msg.channel.send(response)
    else:
        await pld.msg.channel.send(embed=not_found('No statistics to show.'))
