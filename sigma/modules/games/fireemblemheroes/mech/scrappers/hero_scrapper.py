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
import re

import wikitextparser as wtp
from lxml import html


class HeroScrapper(object):
    def __init__(self, scrapper_core):
        self.scrapper = scrapper_core
        self.heroes = {}

    async def scrap_data(self):
        self.scrapper.log.info('Scrapping Heroes...')
        url = self.scrapper.format_link('Hero List')
        data = await self.scrapper.get_page(url)
        data = json.loads(data['data'])
        data = data['mobileview']['sections'][0]['text']
        root = html.fromstring(data)
        hero_list_table = root.cssselect('table.wikitable')[0]
        hero_list = hero_list_table[8:]  # strip the header
        for row in hero_list:
            hero_id = row[1][0].text
            url = row[1][0].attrib['href']
            hero_name = re.sub(r'\([a-zA-Z()\s]+\)', '', hero_id).strip()
            icon = row[0][0][0].attrib['src'].split('?')[0].split('/')
            icon = '/'.join(icon[:5] + icon[6:-1])
            hero_record = {
                'type': 'hero',
                'id': hero_id,
                'url': self.scrapper.wiki_url + url,
                'name': hero_name,
                'icon': icon
            }
            self.heroes.update({hero_id: hero_record})
        for hero in self.heroes.keys():
            if self.scrapper.skip_bio:
                self.heroes[hero]['bio'] = None
            else:
                url = self.scrapper.format_link(hero, raw=True)
                page = await self.scrapper.get_page(url)
                page = wtp.parse(page['data'])
                hero_page_text = self.scrapper.get_template(page, 'HeroPageText')
                bio = self.scrapper.get_value(hero_page_text, 'Background')
                bio = self.scrapper.parse_bio(bio)
                self.heroes[hero]['bio'] = bio
        mega_query = ''.join(self.scrapper.queries)
        query_link = self.scrapper.format_link(mega_query, api=True)
        query_page = await self.scrapper.get_page(query_link)
        query_data = json.loads(query_page['data'])
        results = query_data['query']['results']
        for hero in results:
            self.heroes[hero]['title'] = results[hero]['printouts']['Title'][0]
            self.heroes[hero]['color'] = results[hero]['printouts']['WeaponType'][0].split(' ')[0]
            self.heroes[hero]['weapon type'] = results[hero]['printouts']['WeaponType'][0].split(' ')[1]
            self.heroes[hero]['movement type'] = results[hero]['printouts']['MoveType'][0]
            summon_rarities = results[hero]['printouts']['SummonRarities']
            reward_rarities = results[hero]['printouts']['RewardRarities']
            self.heroes[hero]['rarity'] = self.scrapper.parse_rarity(summon_rarities, reward_rarities)
            skills = {}
            for skill_type in ['weapon', 'assist', 'special']:
                skills[skill_type + 's'] = []
                for tier in range(1, 5):
                    tier = str(tier)
                    if results[hero]['printouts'][skill_type + tier]:
                        skill = results[hero]['printouts'][skill_type + tier][0]['fulltext']
                    else:
                        skill = None
                    unlock = results[hero]['printouts'][skill_type + tier + 'Unlock']
                    if skill and unlock:
                        skill += f' ({unlock[0]}\★)'
                    if skill:
                        skills[skill_type + 's'].append(skill)
                skills[skill_type + 's'] = ', '.join(skills[skill_type + 's'])
            skills['passives'] = {}
            for passive_type in ['A', 'B', 'C']:
                skills['passives'][passive_type] = []
                for tier in range(1, 4):
                    tier = str(tier)
                    skill = results[hero]['printouts']['passive' + passive_type + tier][0] \
                        if results[hero]['printouts']['passive' + passive_type + tier] else None
                    unlock = results[hero]['printouts']['passive' + passive_type + tier + 'Unlock']
                    if skill and unlock:
                        skill += f' ({unlock[0]}\★)'
                    if skill:
                        skills['passives'][passive_type].append(skill)
            passive_skill_lines = []
            for passive_type in skills['passives']:
                if skills['passives'][passive_type]:
                    passive_line = f"`{passive_type}` | {', '.join(skills['passives'][passive_type])}"
                    passive_skill_lines.append(passive_line)
            skills['passives'] = '\n'.join(passive_skill_lines)
            self.heroes[hero]['weapons'] = skills['weapons']
            self.heroes[hero]['assists'] = skills['assists']
            self.heroes[hero]['specials'] = skills['specials']
            self.heroes[hero]['passives'] = skills['passives']
            if results[hero]['printouts']['baseHP']:
                stats = {'5': {'base': [], 'max': []}}
                for stat_type in ['base', 'gp']:
                    values = []
                    for stat in ['HP', 'ATK', 'SPD', 'DEF', 'RES']:
                        value = int(results[hero]['printouts'][stat_type + stat][0])
                        values.append([stat, value])
                    if stat_type == 'base':
                        stats['5'][stat_type] = values
                    else:
                        gp = values
                stats['5']['max'] = self.scrapper.calculate_max_stats('5', stats['5']['base'], gp)
                rarities = []
                for rarity in ['1', '2', '3', '4']:  # Always available in 5⭐
                    value = results[hero]['printouts']['r' + rarity]
                    if value:
                        rarities.append(rarity)
                for rarity in reversed(rarities):
                    previous = str(int(rarity) + 1)
                    previous = stats[previous]['base']
                    stats[rarity] = {}
                    if int(rarity) % 2:
                        values = self.scrapper.calculate_base_stats_odd(previous)
                    else:
                        values = self.scrapper.calculate_base_stats_even(previous)
                    stats[rarity] = {}
                    stats[rarity]['base'] = values
                    stats[rarity]['max'] = self.scrapper.calculate_max_stats(rarity, stats[rarity]['base'], gp)
                self.heroes[hero]['stats'] = stats
                self.heroes[hero]['bst'] = {}
                for rarity in stats:
                    total = 0
                    for stat in stats[rarity]['max']:
                        total += stat[1]
                    self.heroes[hero]['bst'][rarity] = total
            if hero in self.scrapper.aliases['hero'].keys():
                aliases = self.scrapper.aliases['hero'][hero]
            else:
                aliases = []
            self.heroes[hero]['alias'] = aliases
        self.scrapper.log.info('Completed.')
        return self.heroes
