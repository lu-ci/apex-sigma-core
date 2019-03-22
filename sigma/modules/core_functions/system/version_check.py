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

import aiohttp
import yaml
from yaml import YAMLError

from sigma.core.mechanics.event import SigmaEvent


async def version_check(ev: SigmaEvent):
    version_url = 'https://gitlab.com/lu-ci/sigma/apex-sigma/raw/master/info/version.yml'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(version_url) as version_data:
                data = await version_data.read()
                data = yaml.safe_load(data)
    except (aiohttp.ClientConnectorError, YAMLError):
        data = None
    if data:
        official_stamp = data['build_date']
        version = ev.bot.info.get_version()
        current_stamp = version.timestamp
        if official_stamp > current_stamp:
            current = f'{version.major}.{version.minor}.{version.patch} {version.codename}'
            latest = f'{data["version"]["major"]}.{data["version"]["minor"]}.{data["version"]["patch"]}'
            latest += f' {data["codename"]}'
            ev.log.warning('---------------------------------')
            ev.log.warning('Your Sigma version is outdated.')
            ev.log.warning(f'CURRENT: {current}')
            ev.log.warning(f'LATEST:  {latest}')
            ev.log.warning('Updating is strongly suggested.')
            ev.log.warning('---------------------------------')
    else:
        ev.log.warning('Could not retrieve latest version information.')
