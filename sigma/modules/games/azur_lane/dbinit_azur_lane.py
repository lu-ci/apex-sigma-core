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
from lxml import html as lx

from sigma.modules.games.azur_lane.models.azur_lane_ship import AzurLaneShip

url_base = 'https://azurlane.koumakan.jp'


async def basic_index_save(ev, table, table_type, cutter=None, prefix=None):
    """
    Saves a generic iterable HTML table object into AL ship items.
    :type ev: sigma.core.mechanics.even.SigmaEvent
    :type table: lxml.html.HtmlElement
    :type table_type: str
    :type cutter: str
    :type prefix: str
    """
    ev.log.info(f'Updating basic data for {table_type} ships...')
    for row in table[1:]:
        if len(row) in [11, 12]:
            ship_data = AzurLaneShip()
            if cutter and prefix:
                ship_data.id = f'{prefix}_{row[0][0].text.replace(cutter, "")}'
            else:
                ship_data.id = int(row[0][0].text)
            ship_data.url = f'{url_base}{row[0][0].attrib["href"]}'
            ship_data.name = row[1][0].text.strip()
            ship_data.rarity = row[2].text.strip()
            ship_data.type = row[3].text_content().strip()
            ship_data.subtype = row[4][0].text.strip() if len(row) == 12 else None
            ship_data.faction = row[5][0].text.strip() if ship_data.subtype else row[4][0].text.strip()
            await ship_data.save(ev.db)


async def basic_index_fill(ev):
    """
    Fills ship data with basic information from the main ship index.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    ev.log.info('Updating basic Azur Lane ship information...')
    index_url = f'{url_base}/List_of_Ships'
    async with aiohttp.ClientSession() as session:
        async with session.get(index_url) as index_req:
            index_html = await index_req.text()
    index_root = lx.fromstring(index_html)
    normal, planned, collab = index_root.cssselect('.wikitable')[:-1]
    await basic_index_save(ev, normal[0], 'standard')
    await basic_index_save(ev, planned[0], 'Planned', 'Plan', 'planned')
    await basic_index_save(ev, collab[0], 'Collab', 'Collab', 'collab')
    ev.log.info('Updated basic ship data successfully.')


async def detailed_ship_fill(ev):
    """
    Fills detailed ship data by using their pages
    instead of the main index listing basic information.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    ev.log.info('Updating detailed Azur Lane ship information...')
    headers = {'Cookie': 'stopMobileRedirect=true'}
    all_ships = await ev.db.col.AzurLaneShips.find().to_list(None)
    for ship_doc in all_ships:
        ship = AzurLaneShip(ship_doc)
        ev.log.info(f'Parsing {ship.name} details...')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ship.url, headers=headers) as ship_req:
                    ship_html = await ship_req.text()
            ship_root = lx.fromstring(ship_html)
            ship_tabbers = ship_root.cssselect('.tabbertab')
            ship.from_tabbers(ship_tabbers)
            ship_tables = ship_root.cssselect('.wikitable')
            ship.from_tables(ship_tables)
            ship.images.from_etree(ship_root)
            await ship.save(ev.db)
        except Exception as e:
            ev.log.error(f'Failed getting details for {ship.name}: {type(e)} {e}')
    ev.log.info('Updated detailed ship data successfully.')


async def dbinit_azur_lane(ev, force=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type force: bool
    """
    file_count = await ev.db.col.AzurLaneShips.count_documents({})
    if file_count == 0 or force:
        ev.log.info('Updating Azur Lane ship data...')
        await basic_index_fill(ev)
        await detailed_ship_fill(ev)
