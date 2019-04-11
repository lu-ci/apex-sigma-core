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
import discord

from sigma.core.utilities.generic_responses import error, not_found
from sigma.modules.games.azur_lane.models.azur_lane_ship import AzurLaneShip

ship_index_cache = None

rarity_colors = {
    'normal': 0xdcdcdc,
    'rare': 0xb0e0e6,
    'elite': 0xdda0dd,
    'super rare': 0xeee8aa,
    'ultra rare': 0x69ffad
}

faction_prefixes = {
    'sakura empire': 'IJN',
    'eagle union': 'USS',
    'royal navy': 'HMS',
    'ironblood': 'KMS',
    'eastern radiance': 'PRAN',
    'north union': 'SN',
    'iris libre': 'FFNF',
    'vichya dominion': 'MNF'
}

faction_icons = {
    'sakura empire': 'https://azurlane.koumakan.jp/w/images/9/93/Sakuraempire_orig.png',
    'eagle union': 'https://azurlane.koumakan.jp/w/images/2/21/Eagleunion_orig.png',
    'royal navy': 'https://azurlane.koumakan.jp/w/images/8/86/Royalnavy_orig.png',
    'ironblood': 'https://azurlane.koumakan.jp/w/images/f/f5/Ironblood_edited.png',
    'eastern radiance': 'https://azurlane.koumakan.jp/w/images/3/3f/Azurlane-logo-1.png',
    'north union': 'https://i.imgur.com/UdQvZBT.png',
    'iris libre': 'https://i.imgur.com/vVhABbq.png',
    'vichya dominion': 'https://i.imgur.com/L4mBDp9.png'
}


async def get_ship(db, lookup):
    """
    Gets a ship from the given lookup criteria.
    :param db: The database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param lookup: What to search for.
    :type lookup: str
    :return:
    :rtype: dict
    """
    ship = await db[db.db_nam].AzurLaneShips.find_one({'id': lookup})
    if ship is None:
        ship = await db[db.db_nam].AzurLaneShips.find_one({'name': lookup.title()})
        if ship is None:
            all_ships = await db[db.db_nam].AzurLaneShips.find({}).to_list(None)
            for ship_item in all_ships:
                ship_object = AzurLaneShip(ship_item)
                if ship_object.name.lower() == lookup.lower():
                    ship = ship_item
                elif lookup.lower() in ship_object.name.lower():
                    ship = ship_item
                if ship:
                    break
    return ship


async def azurlaneship(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join([pla for pla in pld.args if not pla.startswith('--')])
    no_image = '--no-image' in pld.args
    retrofit = '--retrofit' in pld.args
    awoken = '--awaken' in pld.args
    try:
        lookup = int(lookup)
    except ValueError:
        pass
    if lookup:
        ship = await get_ship(cmd.db, lookup)
        if ship:
            ship = AzurLaneShip(ship)
            response = discord.Embed(color=rarity_colors.get(ship.rarity.lower()))
            response.set_author(name=f'Azur Lane: {ship.name}', icon_url=ship.images.small, url=ship.url)
            if not no_image:
                response.set_image(url=ship.images.main.url)
            for quote in ship.quotes:
                desc_quotes = ['self introduction', 'acquisition']
                if quote.event.lower() in desc_quotes and quote.en:
                    response.description = quote.en
                    break
            if ship.images.chibi:
                response.set_thumbnail(url=ship.images.chibi)
            if retrofit:
                response.add_field(name='Retrofit', value=f'```py\n{ship.stats.retrofit.describe(awoken)}\n```')
            else:
                response.add_field(name='Statistics', value=f'```py\n{ship.stats.normal.describe(awoken)}\n```')
            faction_prefix = faction_prefixes.get(ship.faction.lower())
            faction_icon = faction_icons.get(ship.faction.lower()) or discord.Embed.Empty
            if faction_prefix:
                footer_text = f'{faction_prefix} {ship.name} of the {ship.faction}.'
            else:
                footer_text = f'{ship.name} of the {ship.faction}.'
            response.set_footer(text=footer_text, icon_url=faction_icon)
        else:
            response = not_found('Ship not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
