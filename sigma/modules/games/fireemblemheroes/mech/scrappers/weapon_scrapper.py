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

from lxml import html


class WeaponScrapper(object):
    def __init__(self, scrapper_core):
        self.scrapper = scrapper_core
        self.weapons = {}
        self.plurarize = {
            'Sword': 'Swords',
            'Tome': 'Tomes',
            'Breath': 'Breaths',
            'Lance': 'Lances',
            'Axe': 'Axes',
            'Staff': 'Staves',
            'Bow': 'Bows',
            'Dagger': 'Daggers'
        }
        self.weapon_types = {
            'Red': ['Sword', 'Tome', 'Breath'],
            'Blue': ['Lance', 'Tome', 'Breath'],
            'Green': ['Axe', 'Tome', 'Breath'],
            'Neutral': ['Staff', 'Bow', 'Dagger']
        }

    async def scrap_data(self):
        self.scrapper.log.info('Scrapping Weapons...')
        for color in self.weapon_types:
            for weapon_type in self.weapon_types[color]:
                category = self.plurarize[weapon_type]
                if weapon_type in ['Tome', 'Breath']:
                    category = color + ' ' + category
                mega_query = [
                    f'[[Category:{category}]]',
                    '|?name1',
                    '|?might1',
                    '|?range1',
                    '|?cost1',
                    '|?Is exclusive=exclusive',
                    '|?effect1',
                    '|limit=500',
                ]
                query_string = ''.join(mega_query)
                query_link = self.scrapper.format_link(query_string, api=True)
                query_page = await self.scrapper.get_page(query_link)
                query_data = json.loads(query_page['data'])
                results = query_data['query']['results']
                for weapon_name in results:
                    if results[weapon_name]['printouts']['Effect1']:
                        special_effect = results[weapon_name]['printouts']['Effect1'][0]
                    else:
                        special_effect = None
                    if special_effect:
                        special_effect = special_effect.replace('<br>', ' ')
                        special_effect = special_effect.split(' ')
                        special_effect = [part for part in special_effect if part[:2] != '[[' and part[-2:] != ']]']
                        special_effect = ' '.join(special_effect)
                    url = self.scrapper.format_link(weapon_name)
                    page = await self.scrapper.get_page(url)
                    page = page['data']
                    page = json.loads(page)
                    page = page['mobileview']['sections'][0]['text']
                    root = html.fromstring(page)
                    images = root.cssselect('.hero-infobox a img')
                    image = images[0].attrib['src'].split('?')[0]
                    heroes_with = []
                    for tier in ['4', '3', '2', '1']:
                        escaped_name = weapon_name.replace(' ', '_').replace('+', '%2B')
                        mega_subquery = [
                            '[[Category:Heroes]]',
                            f'[[Has weapon{tier}::{escaped_name} ]]',
                            f'|?Has weapon{tier} unlock=weapon{tier}Unlock'
                        ]
                        subquery_string = ''.join(mega_subquery)
                        subquery_link = self.scrapper.format_link(subquery_string, api=True)
                        subquery_page = await self.scrapper.get_page(subquery_link)
                        subquery_data = json.loads(subquery_page['data'])
                        sub_results = subquery_data['query']['results']
                        if sub_results:
                            for hero in sub_results:
                                if sub_results[hero]['printouts'][f'weapon{tier}Unlock']:
                                    unlock = sub_results[hero]['printouts'][f'weapon{tier}Unlock'][0]
                                else:
                                    unlock = None
                                if unlock:
                                    hero += f' ({unlock}\★)'
                                heroes_with.append(hero)
                            break
                    if weapon_name in self.scrapper.aliases['weapon'].keys():
                        aliases = self.scrapper.aliases['weapon'][weapon_name]
                    else:
                        aliases = []
                    if results[weapon_name]['printouts']['exclusive']:
                        exclusive = True
                    else:
                        exclusive = False
                    weapon = {
                        'type': 'weapon',
                        'id': weapon_name,
                        'name': weapon_name,
                        'color': color,
                        'weapon type': weapon_type,
                        'url': self.scrapper.wiki_url + '/' + weapon_name.replace(' ', '_'),
                        'icon': image,
                        'might': int(results[weapon_name]['printouts']['Might1'][0]),
                        'range': int(results[weapon_name]['printouts']['Range1'][0]),
                        'sp cost': int(results[weapon_name]['printouts']['Cost1'][0]),
                        'exclusive': exclusive,
                        'special effect': special_effect,
                        'heroes with': ', '.join(heroes_with),
                        'alias': aliases
                    }
                    self.weapons[weapon_name] = weapon
        for weapon in self.weapons:
            if weapon + '+' in self.weapons.keys():
                self.weapons[weapon]['see also'] = weapon + '+'
                self.weapons[weapon + '+']['see also'] = weapon
            else:
                self.weapons[weapon]['see also'] = None
        self.scrapper.log.info('Completed.')
        return self.weapons
