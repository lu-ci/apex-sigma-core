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

import secrets

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload
from sigma.core.utilities.stats_processing import add_special_stats


async def table_unflipper(ev: SigmaEvent, pld: MessagePayload):
    if '(╯°□°）╯︵ ┻━┻'.replace(' ', '') in pld.msg.content.replace(' ', ''):
        if pld.msg.guild:
            unflip = bool(pld.settings.get('unflip'))
        else:
            unflip = True
        if unflip:
            await add_special_stats(ev.db, 'tables_fixed')
            table = ['┬─┬ ノ( ^_^ノ)',
                     '┬─┬ ﾉ(° -°ﾉ)',
                     '┬─┬ ノ(゜-゜ノ)',
                     r'┬─┬ ノ(ಠ\_ಠノ)',
                     '┻━┻~~~~  ╯(°□° ╯)',
                     '┻━┻====  ╯(°□° ╯)',
                     r' ┬──┬ ¯\_(ツ)',
                     '(ヘ･_･)ヘ┳━┳',
                     'ヘ(´° □°)ヘ┳━┳']
            table_resp = secrets.choice(table)
            await pld.msg.channel.send(table_resp)
