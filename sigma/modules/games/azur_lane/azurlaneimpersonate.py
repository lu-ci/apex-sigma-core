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
import markovify

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.games.azur_lane.models.azur_lane_ship import AzurLaneShip, get_ship

al_wiki = 'https://azurlane.koumakan.jp'
al_icon = 'https://i.imgur.com/iQ6npWa.png'


async def azurlaneimpersonate(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lookup = ' '.join(pld.args) if pld.args else None
    ship = await get_ship(cmd.db, lookup) if lookup else None
    if ship or lookup is None:
        quotes = []
        if ship:
            sentence_num = 1
            ship = AzurLaneShip(ship)
            for quote in ship.quotes:
                if quote.en:
                    quotes.append(quote.en)
        else:
            sentence_num = 5
            all_ships = await cmd.db[cmd.db.db_nam].AzurLaneShips.find({}).to_list(None)
            for ship_doc in all_ships:
                ship = AzurLaneShip(ship_doc)
                for quote in ship.quotes:
                    if quote.en:
                        quotes.append(quote.en)
        long_quote = ' '.join(quotes)
        sentences = []
        try:
            chain = await cmd.bot.threader.execute(markovify.Text, (long_quote,))
            for _ in range(sentence_num):
                sentence = await cmd.bot.threader.execute(chain.makesentence)
                if sentence:
                    sentences.append(sentence)
        except KeyError:
            sentences = []
        if not sentences:
            not_enough_data = '😖 I could not think of anything...'
            response = discord.Embed(color=0xBE1931, title=not_enough_data)
        else:
            response = discord.Embed(color=0xbdddf4)
            if lookup:
                response.set_author(name=f'{ship.faction} {ship.name}', icon_url=ship.images.small, url=ship.url)
            else:
                response.set_author(name='Azur Lane', icon_url=al_icon, url=al_wiki)
            response.description = ' '.join(sentences)
    else:
        response = GenericResponse('Ship not found.').not_found()
    await pld.msg.channel.send(embed=response)
