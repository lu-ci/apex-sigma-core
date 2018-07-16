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

import aiohttp
import yaml

from sigma.core.mechanics.event import SigmaEvent


async def dbinit_items(ev: SigmaEvent, force=False):
    await dbinit_item_data(ev, force)
    await dbinit_recipe_data(ev, force)


async def dbinit_item_data(ev: SigmaEvent, force=False):
    doc_count = await ev.db[ev.db.db_nam].ItemData.count_documents({})
    if not doc_count or force:
        file_url = 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/items/item_core_manifest.yml'
        ev.log.info('Updating profession item files.')
        await ev.db[ev.db.db_nam].ItemData.drop()
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as data_response:
                data = await data_response.read()
                data = yaml.safe_load(data)
        await ev.db[ev.db.db_nam].ItemData.insert_many(data)
        ev.log.info('Updated profession item files successfully.')


async def dbinit_recipe_data(ev: SigmaEvent, force=False):
    doc_count = await ev.db[ev.db.db_nam].RecipeData.count_documents({})
    if not doc_count or force:
        file_url = 'https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/items/recipe_core_manifest.yml'
        ev.log.info('Updating cooking recipe files.')
        await ev.db[ev.db.db_nam].RecipeData.drop()
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as data_response:
                data = await data_response.read()
                data = yaml.safe_load(data)
        await ev.db[ev.db.db_nam].RecipeData.insert_many(data)
        ev.log.info('Updated cooking recipe files successfully.')
