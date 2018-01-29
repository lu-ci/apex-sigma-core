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


class AssistScrapper(object):
    def __init__(self, scrapper_core):
        self.scrapper = scrapper_core
        self.assists = {}

    async def scrap_data(self):
        self.scrapper.log.info('Scrapping Assists...')
        mega_query = [
            '[[Category:Assists]]',
            '|?name1',
            '|?range1',
            '|?effect1',
            '|?cost1',
            '|?Has weapon restriction=wpnRestrict',
            '|?Is exclusive=exclusive',
            '|limit=100'
        ]
        query_string = ''.join(mega_query)
        query_link = self.scrapper.format_link(query_string, api=True)
        query_page = await self.scrapper.get_page(query_link)
        query_data = json.loads(query_page['data'])
        results = query_data['query']['results']
        for assist in results:
            effect = results[assist]['printouts']['Effect1'][0].replace('<br>', ' ')
            inherit_restriction = results[assist]['printouts']['wpnRestrict']
            if inherit_restriction:
                inherit_restriction = inherit_restriction[0]
            else:
                if results[assist]['printouts']['exclusive'][0] == 't':
                    inherit_restriction = 'Is exclusive'
                else:
                    raise Exception
            heroes_with = []
            escaped_name = assist.replace(' ', '_')
            for tier in ['1', '2', '3']:
                mega_subquery = [
                    "[[Category:Heroes]]"
                    f"[[Has assist{tier}::{escaped_name} ]]",
                    f"|?Has assist{tier} unlock=assist{tier}Unlock"
                ]
                subquery_string = ''.join(mega_subquery)
                subquery_link = self.scrapper.format_link(subquery_string, api=True)
                subquery_page = await self.scrapper.get_page(subquery_link)
                subquery_data = json.loads(subquery_page['data'])
                sub_results = subquery_data['query']['results']
                if sub_results:
                    for hero in sub_results:
                        unlock = sub_results[hero]['printouts'][f'assist{tier}Unlock']
                        if unlock:
                            hero += f' ({unlock[0]}★)'
                        heroes_with.append(hero)
                    break
            heroes_with = ', '.join(heroes_with)
            self.assists[assist] = {
                'type': 'assist',
                'id': assist,
                'name': assist,
                'url': self.scrapper.wiki_url + '/' + assist.replace(' ', '_'),
                'range': results[assist]['printouts']['Range1'][0],
                'effect': effect,
                'sp cost': results[assist]['printouts']['Cost1'][0],
                'inherit restriction': inherit_restriction,
                'heroes with': heroes_with
            }
        self.scrapper.log.info('Completed.')
        return self.assists
