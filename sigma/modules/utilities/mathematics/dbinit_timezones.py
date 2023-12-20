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

import aiohttp
import yaml


async def dbinit_timezones(ev, force=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type force: bool
    """
    doc_count = await ev.db[ev.db.db_name].TimezoneData.count_documents({})
    if not doc_count or force:
        file_urls = {
            'tz_alias': 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/timezones/tz_aliases.yml',
            'tz_offset': 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/timezones/tz_offsets.yml'
        }
        ev.log.info('Updating timezone files.')
        await ev.db[ev.db.db_name].TimezoneData.drop()
        documents = []
        for key in file_urls.keys():
            file_url = file_urls.get(key)
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as data_response:
                    data = await data_response.read()
                    data = yaml.safe_load(data)
            for dkey in data.keys():
                doc_data = {
                    'type': key,
                    'zone': dkey,
                    'value': data.get(dkey)
                }
                documents.append(doc_data)
        await ev.db[ev.db.db_name].TimezoneData.insert_many(documents)
        ev.log.info('Updated timezone files successfully.')
