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


async def dbinit_shootfoot(ev, force=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type force: bool
    """
    doc_count = await ev.db.col.ShootFootData.count_documents({})
    if not doc_count or force:
        file_url = 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/jokes/feets.yml'
        ev.log.info('Updating foot shooting files.')
        await ev.db.col.ShootFootData.drop()
        documents = []
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as data_response:
                data = await data_response.read()
                data = yaml.safe_load(data)
        for lang in data.keys():
            lang_low = lang.lower()
            methods = data.get(lang)
            aliases = data.get('alts')
            doc_data = {'lang': lang, 'lang_low': lang_low, 'methods': methods, 'alts': aliases}
            documents.append(doc_data)
        await ev.db.col.ShootFootData.insert_many(documents)
        ev.log.info('Updated foot shooting files successfully.')
