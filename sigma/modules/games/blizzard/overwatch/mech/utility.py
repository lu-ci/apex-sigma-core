# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import asyncio

from overwatch_api.core import AsyncOWAPI

ow_cli = AsyncOWAPI(request_timeout=60)
ow_icon = 'https://i.imgur.com/YZ4w2ey.png'
region_convert = {
    'europe': 'eu',
    'korea': 'kr',
    'na': 'us',
    'americas': 'us',
    'america': 'us',
    'china': 'cn',
    'japan': 'jp'
}


def clean_numbers(stats: dict):
    for key in stats:
        try:
            int_value = int(stats.get(key))
            if int_value != stats.get(key):
                int_value = round(stats.get(key), 2)
            stats.update({key: int_value})
        except ValueError:
            pass
        except TypeError:
            pass
    return stats


async def get_profile(battletag: str, region: str):
    profile = None
    timeout = False
    failed = False
    # noinspection PyBroadException
    try:
        profile = await ow_cli.get_profile(battletag, regions=region)
    except asyncio.TimeoutError:
        timeout = True
    except Exception:
        failed = True
    return profile, timeout, failed
