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

from sigma.core.mechanics.event import SigmaEvent


def clean_entries(entries):
    """

    :param entries:
    :type entries:
    """
    to_remove = []
    for entry in entries:
        joke_body = entry.get('body')
        if not joke_body or len(joke_body) >= 1024:
            to_remove.append(entry)
    [entries.remove(x) for x in to_remove]


async def dbinit_jokes(ev: SigmaEvent, force=False):
    """

    :param ev:
    :type ev:
    :param force:
    :type force:
    """
    doc_count = await ev.db[ev.db.db_nam].JokeData.count_documents({})
    if not doc_count or force:
        file_urls = [
            'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/jokes/wocka.json',
            'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/jokes/stupidstuff.json'
        ]
        ev.log.info('Updating joke data files.')
        await ev.db[ev.db.db_nam].JokeData.drop()
        documents = []
        for file_url in file_urls:
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as data_response:
                    data = await data_response.read()
                    data = json.loads(data)
            documents += data
        clean_entries(documents)
        await ev.db[ev.db.db_nam].JokeData.insert_many(documents)
        ev.log.info('Updated joke data files successfully.')
