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

import json
import aiohttp

from sigma.core.mechanics.event import SigmaEvent


async def dbinit_dictionary(ev: SigmaEvent, force=False):
    doc_count = await ev.db[ev.db.db_nam].DictionaryData.count()
    if not doc_count or force:
        file_url = 'https://gitlab.com/lu-ci/apex-sigma-res/raw/master/dictionary/dictionary.json'
        ev.log.info('Updating dictionary files.')
        await ev.db[ev.db.db_nam].DictionaryData.drop()
        documents = []
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as data_response:
                data = await data_response.read()
                data = json.loads(data)
        for dkey in data.keys():
            doc_data = {'word': dkey.lower(), 'description': data.get(dkey)}
            documents.append(doc_data)
        await ev.db[ev.db.db_nam].DictionaryData.insert_many(documents)
        ev.log.info('Updated dictionary files successfully.')
