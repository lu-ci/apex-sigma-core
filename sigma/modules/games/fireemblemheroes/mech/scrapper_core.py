import re

import aiohttp
import arrow
import yaml

from sigma.core.mechanics.logger import create_logger
from .scrappers.assist_scrapper import AssistScrapper
from .scrappers.hero_scrapper import HeroScrapper
from .scrappers.passive_scrapper import PassiveScrapper
from .scrappers.special_scrapper import SpecialScrapper
from .scrappers.weapon_scrapper import WeaponScrapper


class ScrapperContainer(object):
    def __init__(self, scrapper_core):
        self.core = scrapper_core
        self.hero = HeroScrapper(self.core)
        self.weapon = WeaponScrapper(self.core)
        self.assist = AssistScrapper(self.core)
        self.special = SpecialScrapper(self.core)
        self.passive = PassiveScrapper(self.core)


class FEHScrapper(object):
    def __init__(self, feh):
        self.feh = feh
        self.log = create_logger('FEH Scrapper')
        self.db = self.feh.db
        self.data_dir = self.feh.data_dir
        self.wiki_cache = self.db[self.db.db_cfg.database].FEHWikiCache
        self.feh_db = self.db[self.db.db_cfg.database].FEHData
        self.wiki_url = 'https://feheroes.gamepedia.com'
        self.no_cache = False
        self.skip_bio = False
        self.hero_data = None
        self.weapon_data = None
        self.assist_data = None
        self.special_data = None
        self.passive_data = None
        self.aliases = self.get_yaml_data(self.feh.data_dir + '/aliases.yml')
        self.growth = self.get_yaml_data(self.data_dir + '/growth.yml')
        self.queries = self.get_yaml_data(self.data_dir + '/queries.yml')
        self.scrappers = ScrapperContainer(self)

    @staticmethod
    def get_yaml_data(location):
        with open(location, encoding='utf-8') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        return yaml_data

    @staticmethod
    def format_link(page, raw=False, api=False, sections='0'):
        if page[0] != '/':
            url = f'/{page}'
        else:
            url = page
        if raw:
            url += '?action=raw'
        elif api:
            url = f'/api.php?action=ask&format=json&query={page}'
        else:
            url = '/api.php'
            url += '?action=mobileview'
            url += '&format=json'
            url += f'&sections={sections}'
            url += '&notransform=true'
            url += '&onlyrequestedsections=true'
            url += f'&page={page}'
        return url

    async def get_page(self, url):
        cache = await self.wiki_cache.find_one({'url': url})
        if cache and not self.no_cache:
            record = cache
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.wiki_url + url) as data_response:
                    data = await data_response.text()
            record = {
                'url': url,
                'data': data,
                'timestamp': arrow.utcnow().timestamp
            }
            await self.wiki_cache.insert_one(record)
        return record

    @staticmethod
    def get_template(markup, name):
        output = None
        for template in markup.templates:
            if template.name.strip() == name.strip():
                output = template
                break
        return output

    @staticmethod
    def get_argument(template, name):
        output = None
        for argument in template.arguments:
            if argument.name.strip() == name.strip():
                output = argument
                break
        return output

    def get_value(self, *args):
        if len(args) == 1:
            raise Exception('Not enough arguments.')
        elif len(args) == 2:
            template = args[0]
            argument = args[1]
        elif len(args) == 3:
            markup = args[0]
            template_arg = args[1]
            template = self.get_template(markup, template_arg)
            argument = args[2]
        else:
            raise Exception('Too many arguments.')
        argument = self.get_argument(template, argument)
        if argument:
            value = argument.value
            if isinstance(value, str):
                value = value.strip()
                if value == '':
                    value = None
            return value
        else:
            return None

    def get_range(self, markup, template, argument, starting_from=1):
        indexes = []
        template = self.get_template(markup, template)
        if not template:
            return indexes
        while self.get_argument(template, argument + str(starting_from)):
            index = self.get_argument(template, argument + str(starting_from))
            if index:
                indexes.append(str(starting_from))
            starting_from += 1
        return indexes

    def parse_bio(self, bio):
        if bio:
            for match in re.findall(r'\[{2}[a-zA-Z\s()|]+\]{2}', bio):
                link = match[2:-2].split('|')
                if len(link) > 1:
                    text = link[1]
                else:
                    text = link[0]
                link = link[0].replace(' ', '_')
                bio = bio.replace(match, f"[{text}]({self.wiki_url + '/' + link})")
            bio = bio.strip().replace('))', '\\))')  # Escape the links
        return bio

    @staticmethod
    def parse_rarity(summon_rarities, reward_rarities):
        if summon_rarities:
            if len(summon_rarities) > 1:
                rarity = f'{summon_rarities[0]}★ - {summon_rarities[-1]}★'
            else:
                rarity = f'{summon_rarities[0]}★'
        elif reward_rarities:
            if len(reward_rarities) > 1:
                rarity = f'{reward_rarities[0]}★ - {reward_rarities[-1]}★'
            else:
                rarity = f'{reward_rarities[0]}★'
        else:
            rarity = 'N/A'
        return rarity

    @staticmethod
    def sort_stats(stats):
        keys = [stat[0] for stat in stats]
        sorted_stats = []
        for stat in ['HP', 'ATK', 'SPD', 'DEF', 'RES']:
            sorted_stats.append([stat, stats[keys.index(stat)][1]])
        return sorted_stats

    def calculate_base_stats_down(self, stats, is_odd=True):
        stats = self.sort_stats(stats)
        if not is_odd:
            hp = stats[0][1] - 1
        else:
            hp = stats[0][1]
        rest = stats[1:]
        if not is_odd:
            rest = reversed(rest)
        rest = sorted(rest, key=lambda stat: stat[1], reverse=is_odd)  # Sort the stats
        for index in range(0, 2):
            rest[index][1] -= 1
        calculated_stats = rest
        calculated_stats.append(['HP', hp])
        calculated_stats = self.sort_stats(calculated_stats)
        return calculated_stats

    def calculate_base_stats_even(self, stats):
        output = self.calculate_base_stats_down(stats, False)
        return output

    def calculate_base_stats_odd(self, stats):
        output = self.calculate_base_stats_down(stats, True)
        return output

    def calculate_max_stats(self, rarity, base, gp):
        max_stats = []
        for index, stat in enumerate(['HP', 'ATK', 'SPD', 'DEF', 'RES']):
            value = base[index][1] + self.growth[int(rarity)][gp[index][1]]
            max_stats.append([stat, value])
        return max_stats

    async def scrap_all(self):
        # noinspection PyBroadException
        try:
            hero_data = await self.scrappers.hero.scrap_data()
            weapon_data = await self.scrappers.weapon.scrap_data()
            assist_data = await self.scrappers.assist.scrap_data()
            special_data = await self.scrappers.special.scrap_data()
            passive_data = await self.scrappers.passive.scrap_data()
            scrapped_data = [hero_data, weapon_data, assist_data, special_data, passive_data]
        except Exception:
            self.log.error('Scrapper Failed!')
            scrapped_data = []
        return scrapped_data
