# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


class PassiveScrapper(object):
    def __init__(self, scrapper_core):
        self.scrapper = scrapper_core
        self.passives = {}

    async def scrap_data(self):
        self.scrapper.log.info('Scrapping Passives...')
        prim_link = self.scrapper.format_link('Passives', sections='1|2|3|4')
        prim_page = await self.scrapper.get_page(prim_link)
        prim_data = json.loads(prim_page['data'])
        sections = prim_data['mobileview']['sections']
        for index, passive_type in enumerate(['A', 'B', 'C', 'S']):
            sections[index]['passive type'] = passive_type
        for section in sections:
            table = html.fromstring(section['text']).cssselect('table')[0]
            for row in table[5:]:
                name = row[1][0].text.strip()
                heroes_with = []
                passive_type = section['passive type']
                escaped_name = name.replace('+', '%2B')
                if passive_type != 'S':  # Seals are universal
                    sub_results = None
                    if name[-1] in ['1', '2', '3']:
                        tier = name[-1]
                    else:
                        tier = '3'
                    while not sub_results:
                        mega_subquery = [
                            "[[Category:Heroes]]",
                            f"[[Has passive{passive_type}{tier}::{escaped_name} ]]",
                            f"|?Has passive{passive_type}{tier} unlock=passive{passive_type}{tier}Unlock"
                        ]
                        subquery_string = ''.join(mega_subquery)
                        subquery_link = self.scrapper.format_link(subquery_string, api=True)
                        subquery_page = await self.scrapper.get_page(subquery_link)
                        subquery_data = json.loads(subquery_page['data'])
                        sub_results = subquery_data['query']['results']
                        if sub_results:
                            for hero in sub_results:
                                unlock = sub_results[hero]['printouts'][f'passive{passive_type}{tier}Unlock']
                                if unlock:
                                    hero += f' ({unlock[0]}★)'
                                heroes_with.append(hero)
                            break
                        else:
                            tier = '1' if tier == '3' else str(int(tier) + 1)
                heroes_with = ', '.join(heroes_with)

                self.passives[name] = {
                    'type': 'passive',
                    'passive type': section['passive type'],
                    'id': name,
                    'name': name,
                    'url': self.scrapper.wiki_url + '/' + name.replace(' ', '_'),
                    'icon': row[0][0][0].attrib['src'].split('?')[0],
                    'effect': row[2].text.strip(),
                    'sp cost': int(row[3].text) if row[3].text else row[3].text,
                    'inherit restriction': row[4].text,
                    'heroes with': heroes_with if heroes_with else None
                }
        tetr_string = '[[Category:Passives]][[Has seal::true]]|?name1|?name2|?name3|limit=100'
        tetr_link = self.scrapper.format_link(tetr_string, api=True)
        tetr_page = await self.scrapper.get_page(tetr_link)
        tetr_data = json.loads(tetr_page['data'])
        tetr_results = tetr_data['query']['results']
        for passive in tetr_results:
            for index in ['1', '2', '3']:
                if tetr_results[passive]['printouts']['Name' + index]:
                    name = tetr_results[passive]['printouts']['Name' + index][0]
                else:
                    name = None
                if name:
                    if self.passives[name]['passive type'] != 'S':
                        self.passives[name]['passive type'] += ', S'
        for passive in self.passives:
            see_also = []
            if passive[-1] in ['1', '2', '3']:
                prev_lvl = str(int(passive[-1]) - 1)
                next_lvl = str(int(passive[-1]) + 1)
                while prev_lvl != '0':
                    prev_lvl_passive = passive[:-1] + prev_lvl
                    exists = prev_lvl_passive in self.passives.keys()
                    if exists:
                        see_also.append(prev_lvl_passive)
                    prev_lvl = str(int(prev_lvl) - 1)
                while next_lvl != '4':
                    next_lvl_passive = passive[:-1] + next_lvl
                    exists = next_lvl_passive in self.passives.keys()
                    if exists:
                        see_also.append(next_lvl_passive)
                    next_lvl = str(int(next_lvl) + 1)
            alias = []
            if passive[-1] in ['1', '2', '3']:
                next_lvl = str(int(passive[-1]) + 1)
                next_lvl_passive = passive[:-1] + next_lvl
                if next_lvl_passive in self.passives.keys():
                    exists = True
                else:
                    exists = False
                if not exists:
                    alias.append(passive[:-1].replace('+', '').strip())
            self.passives[passive]['see also'] = ', '.join(see_also) if see_also else None
            self.passives[passive]['alias'] = alias
        self.scrapper.log.info('Completed.')
        return self.passives
