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
import discord
from lxml import html

ABBR_MAP = {
    'PlayStation': 'PS1',
    'PlayStation 2': 'PS2',
    'PlayStation 3': 'PS3',
    'PlayStation 4': 'PS4',
    'PlayStation 5': 'PS5',
    'PlayStation Portable': 'PSP',
    'PlayStation Vita': 'PS Vita'
}

PLATFORMS = {
    'playstation': ['ps1', 'psx', 'ps'],
    'playstation 2': ['ps2'],
    'playstation 3': ['ps3'],
    'playstation 4': ['ps4'],
    'playstation 5': ['ps5'],
    'playstation vita': ['ps vita', 'psv'],
    'psp': ['playstation portable'],
    'xbox': [],
    'xbox 360': [],
    'xbox one': ['xbone'],
    'xbox series-x': ['xbox x'],
    'ds': ['nintendo ds'],
    '3ds': ['nintendo 3ds'],
    'wii': ['nintendo wii'],
    'wii u': ['nintendo wii u'],
    'switch': ['nintendo switch'],
    'game boy advance': ['gba'],
    'gamecube': [],
    'nintendo 64': ['n64'],
    'dreamcast': [],
    'ios': ['iphone', 'ipad', 'ipod'],
    'pc': []
}


class MetaCriticGame(object):
    """
    The framework for retrieving and parsing MetaCritic game data.
    """

    __slots__ = (
        'logo', 'headers', 'base_url',
        'formed_url', 'data', 'valid_response'
    )

    def __init__(self, cmd):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        """
        self.logo = 'https://i.imgur.com/hZIlicx.png'
        self.headers = cmd.bot.get_agent()
        self.base_url = 'http://www.metacritic.com'
        self.formed_url = None
        self.data = None
        self.valid_response = True

    @staticmethod
    def get_platform(platform):
        """
        Gets the correct platform name, if it exists.
        :type platform: str
        :rtype: str
        """
        match = None
        platform = platform.replace('-', ' ')
        for name, alt in PLATFORMS.items():
            if platform == name or platform in alt:
                match = name
                break
        return match

    @staticmethod
    def path_from_args(args):
        """
        Creates a URL path from the given arguments.
        :type args: list[str]
        :rtype: str
        """
        cleaned_args = []
        for arg in args:
            cleaned_arg = ''
            for char in arg:
                if char.isalpha() or char.isdigit():
                    cleaned_arg += char
                elif char in [' ', '-']:
                    cleaned_arg += '-'
            cleaned_args.append(cleaned_arg)
        return '/'.join(cleaned_args)

    def generate_embed(self):
        """
        Generates the command embed.
        :rtype: discord.Embed
        """
        embed = discord.Embed(color=0xffcc34, description=f'Released on {self.extract_release_date()}')
        embed.set_author(name=self.extract_title(), url=self.formed_url, icon_url=self.logo)
        embed.set_thumbnail(url=self.extract_image())
        platforms = self.extract_platforms()
        if platforms:
            embed.set_footer(text=f'Also on: {self.extract_platforms()}')

        meta_score = self.extract_meta_score()
        c_pos, c_mix, c_neg = self.extract_critic_scores()
        critic_text = f'Overall: {meta_score}\nPositive: {c_pos}\n'
        critic_text += f'Mixed: {c_mix}\nNegative: {c_neg}'
        embed.add_field(name='Metascore', value=critic_text)

        user_score = self.extract_user_score()
        u_pos, u_mix, u_neg = self.extract_user_scores()
        user_text = f'Overall: {user_score}\nPositive: {u_pos}\n'
        user_text += f'Mixed: {u_mix}\nNegative: {u_neg}'
        embed.add_field(name='User Score', value=user_text)

        return embed

    async def set_response_data(self, *args):
        """
        Makes the request and sets the response data.
        :type args: list[str] or str
        """
        url_path = self.path_from_args(args)
        self.formed_url = f'{self.base_url}/{url_path}'
        async with aiohttp.ClientSession() as session:
            async with session.get(self.formed_url, headers=self.headers) as response:
                self.data = html.fromstring(await response.read())
                self.valid_response = response.status == 200

    def extract_title(self):
        """
        Extracts the title from the response data.
        :rtype: str
        """
        title_obj = self.data.cssselect('.product_title a h1')[0]
        return title_obj.text_content()

    def extract_image(self):
        """
        Extracts the image from the response data.
        :rtype: str
        """
        image_obj = self.data.cssselect('img.product_image.large_image')[0]
        return image_obj.attrib['src']

    def extract_release_date(self):
        """
        Extracts the release date from the response data.
        :rtype: str
        """
        release_obj = self.data.cssselect('.release_data .data')[0]
        return release_obj.text_content()

    def extract_platforms(self):
        """
        Extracts the platforms from the response data.
        :rtype: str
        """
        platforms_obj = self.data.cssselect('.product_platforms .data')
        platforms = []
        if platforms_obj:
            for obj in platforms_obj[0]:
                platform = ABBR_MAP.get(obj.text_content(), obj.text_content())
                platforms.append(platform)
        return ', '.join(platforms)

    def extract_meta_score(self):
        """
        Extracts the metascore from the response data.
        :rtype: str
        """
        meta_score_obj = self.data.cssselect('.metascore_w.xlarge')
        if meta_score_obj:
            meta_score = meta_score_obj[0].text_content()
        else:
            meta_score = 'None'
        return meta_score

    def extract_user_score(self):
        """
        Extracts the user score from the response data.
        :rtype: str
        """
        user_score_obj = self.data.cssselect('.metascore_w.user')
        if user_score_obj:
            user_score = user_score_obj[0].text_content()
        else:
            user_score = 'None'
        return user_score

    def extract_critic_scores(self):
        """
        Extracts the critic review totals from the response data.
        :rtype: str, str, str
        """
        score_obj = self.data.cssselect('.score_counts')[0].getchildren()
        pos = score_obj[0].cssselect('.count')[0].text_content()
        mix = score_obj[1].cssselect('.count')[0].text_content()
        neg = score_obj[2].cssselect('.count')[0].text_content()
        return pos, mix, neg

    def extract_user_scores(self):
        """
        Extracts the user review totals from the response data.
        :rtype: str, str, str
        """
        score_obj = self.data.cssselect('.score_counts')[1].getchildren()
        pos = score_obj[0].cssselect('.count')[0].text_content()
        mix = score_obj[1].cssselect('.count')[0].text_content()
        neg = score_obj[2].cssselect('.count')[0].text_content()
        return pos, mix, neg


class MetaCriticMusic(MetaCriticGame):
    """
    The framework for retrieving and parsing MetaCritic music data.
    """

    def __init__(self, cmd):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        """
        super().__init__(cmd)

    def extract_title(self):
        """
        Extracts the title from the response data.
        :rtype: str
        """
        title_obj = self.data.cssselect('.product_title a h1')[0]
        artist_obj = self.data.cssselect('.band_name')[0]
        return f'{title_obj.text_content()} - {artist_obj.text_content()}'

    def extract_release_date(self):
        """
        Extracts the release date from the response data.
        :rtype: str
        """
        release_obj = self.data.cssselect('.summary_detail.release .data')[0]
        return release_obj.text_content()


class MetaCriticMovie(MetaCriticGame):
    """
    The framework for retrieving and parsing MetaCritic movie and tv data.
    """

    def __init__(self, cmd):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        """
        super().__init__(cmd)

    def extract_title(self):
        """
        Extracts the title from the response data.
        :rtype: str
        """
        title_obj = self.data.cssselect('.product_page_title h1')[0]
        return title_obj.text_content()

    def extract_image(self):
        """
        Extracts the image from the response data.
        :rtype: str
        """
        image_obj = self.data.cssselect('.summary_img')[0]
        return image_obj.attrib['src']

    def extract_release_date(self):
        """
        Extracts the release date from the response data.
        :rtype: str
        """
        release_obj = self.data.cssselect('.release_date')[0][1]
        return release_obj.text_content()

    def extract_meta_score(self):
        """
        Extracts the metascore from the response data.
        :rtype: str
        """
        meta_score_obj = self.data.cssselect('.metascore_w.larger')
        if meta_score_obj:
            meta_score = meta_score_obj[0].text_content()
        else:
            meta_score = 'None'
        return meta_score

    def extract_critic_scores(self):
        """
        Extracts the critic review totals from the response data.
        :rtype: str, str, str
        """
        score_obj = self.data.cssselect('.distribution')[0]
        pos = score_obj.cssselect('.chart.positive .count.fr')[0].text_content()
        mix = score_obj.cssselect('.chart.mixed .count.fr')[0].text_content()
        neg = score_obj.cssselect('.chart.negative .count.fr')[0].text_content()
        return pos, mix, neg

    def extract_user_scores(self):
        """
        Extracts the user review totals from the response data.
        :rtype: str, str, str
        """
        score_obj = self.data.cssselect('.distribution')[1]
        pos = score_obj.cssselect('.chart.positive .count.fr')[0].text_content()
        mix = score_obj.cssselect('.chart.mixed .count.fr')[0].text_content()
        neg = score_obj.cssselect('.chart.negative .count.fr')[0].text_content()
        return pos, mix, neg


class MetaCriticSearch(object):
    """
    The framework for retrieving and parsing MetaCritic search data.
    """

    __slots__ = (
        'logo', 'headers', 'base_url', 'formed_url', 'data',
        'valid_response', 'search_query', 'result_map', 'results_len'
    )

    def __init__(self, cmd):
        """
        :param cmd: The command instance.
        :type cmd: sigma.core.mechanics.command.SigmaCommand
        """
        self.logo = 'https://i.imgur.com/hZIlicx.png'
        self.headers = cmd.bot.get_agent()
        self.base_url = 'http://www.metacritic.com'
        self.formed_url = None
        self.data = None
        self.valid_response = True
        self.search_query = None
        self.result_map = {}
        self.results_len = 0

    @staticmethod
    def path_from_args(args):
        """
        Creates a URL path from the given arguments.
        :type args: list[str]
        :rtype: str
        """
        cleaned_args = []
        for arg in args:
            arg = arg.replace(' ', '-').replace(':', '').strip()
            cleaned_args.append(arg)
        cleaned_args.append('results')
        return '/'.join(cleaned_args)

    def generate_embed(self, category=None):
        """
        Generates the command embed.
        :rtype: discord.Embed
        """
        embed = discord.Embed(color=0xffcc34, description=self.extract_results(category))
        embed.set_author(name=f'Results for {self.search_query}', url=self.formed_url, icon_url=self.logo)
        embed.set_footer(text='Reply with a number to select a result.')
        return embed

    async def set_response_data(self, *args):
        """
        Makes the request and sets the response data.
        :type args: list[str] or str
        """
        url_path = self.path_from_args(args)
        self.search_query = url_path.split('/')[2]
        self.formed_url = f'{self.base_url}/{url_path}'
        async with aiohttp.ClientSession() as session:
            async with session.get(self.formed_url, headers=self.headers) as response:
                self.data = html.fromstring(await response.read())
                self.valid_response = response.status == 200

    def extract_game_data(self, result_obj):
        """
        Extracts the game specific details from the response data.
        :rtype: list[str], str
        """
        result_data = result_obj.cssselect('.main_stats')[0]
        score = result_data[0].text_content()
        url = self.base_url + result_data[-2][0].attrib['href']
        title = result_data[-2][0].text_content().strip()
        platform = result_data[-1][0].text_content().strip()
        year = result_data[-1].text_content().split('\n')[-1].strip('\n').strip()
        platform_year = f'{platform}, {year}'
        data = [title, url, platform_year, score]
        href = result_data[-2][0].attrib['href'].lstrip('/')
        return data, href

    def extract_data(self, result_obj):
        """
        Extracts the general details from the response data.
        :rtype: list[str], str
        """
        result_data = result_obj.cssselect('.main_stats')[0]
        score = result_data[0].text_content()
        url = self.base_url + result_data[-2][0].attrib['href']
        title = result_data[-2][0].text_content().strip()
        year = result_data[-1].text_content().split('\n')[-1].strip('\n').strip()
        data = [title, url, year, score]
        href = result_data[-2][0].attrib['href'].lstrip('/')
        return data, href

    def extract_results(self, category):
        """
        Extracts the search results from the response data.
        :rtype: str
        """
        results_obj = self.data.cssselect('.search_results.module .result')
        results_data = []
        results_href = []
        for result_obj in results_obj:
            # noinspection PyBroadException
            try:
                if category == 'game':
                    data, href = self.extract_game_data(result_obj)
                else:
                    data, href = self.extract_data(result_obj)
                results_data.append(data)
                results_href.append(href)
            except Exception:
                pass
        results = []
        for num, result_data in enumerate(results_data):
            title, url, details, score = result_data
            result_str = f'**{num + 1}.** [{title}]({url}) ({details}) - {score}'
            results.append(result_str)
        self.results_len = len(results)
        for num, href in enumerate(results_href):
            self.result_map.update({str(num + 1): href})
        return '\n'.join(results)
