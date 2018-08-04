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

import secrets

import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.stats_processing import add_special_stats


async def table_unflipper(ev: SigmaEvent, message: discord.Message):
    if '(╯°□°）╯︵ ┻━┻'.replace(' ', '') in message.content.replace(' ', ''):
        if message.guild:
            unflip = bool(await ev.db.get_guild_settings(message.guild.id, 'unflip'))
        else:
            unflip = True
        if unflip:
            await add_special_stats(ev.db, 'tables_fixed')
            table = ['┬─┬ ノ( ^_^ノ)',
                     '┬─┬ ﾉ(° -°ﾉ)',
                     '┬─┬ ノ(゜-゜ノ)',
                     '┬─┬ ノ(ಠ\_ಠノ)',
                     '┻━┻~~~~  ╯(°□° ╯)',
                     '┻━┻====  ╯(°□° ╯)',
                     ' ┬──┬ ¯\_(ツ)',
                     '(ヘ･_･)ヘ┳━┳',
                     'ヘ(´° □°)ヘ┳━┳']
            table_resp = secrets.choice(table)
            await message.channel.send(table_resp)
