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

import json

import aiohttp


async def dbinit_httpstatus(ev, force=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type force: bool
    """
    doc_count = await ev.db[ev.db.db_nam].HTTPStatusData.count_documents({})
    if not doc_count or force:
        file_url = 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/http/http_status.json'
        ev.log.info('Updating HTTP status files.')
        await ev.db[ev.db.db_nam].HTTPStatusData.drop()
        documents = []
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as data_response:
                data = await data_response.read()
                data = json.loads(data)
        for key, value in data.items():
            if not isinstance(value, list):
                value = [value]
            doc_data = {
                'code': key,
                'messages': value
            }
            documents.append(doc_data)
        await ev.db[ev.db.db_nam].HTTPStatusData.insert_many(documents)
        ev.log.info('Updated HTTP status files successfully.')
