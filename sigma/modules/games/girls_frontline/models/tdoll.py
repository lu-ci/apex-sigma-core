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
import lxml.html as lx

STAT_LOCATIONS = {
    'health': [0, 0, 0, 1, 0, 2],
    'ammo': [0, 0, 0, 1, 1],
    'ration': [0, 0, 0, 1, 2],
    'damage': [1, 0, 0, 0, 1, 0, 0, 0, -1],
    'evasion': [1, 0, 0, 0, 3, 0, 0, 0, -1],
    'accuracy': [1, 0, 0, 1, 1, 0, 0, 0, -1],
    'rate_of_fire': [1, 0, 0, 1, 3, 0, 0, 0, -1],
    'move_speed': [1, 0, 0, 2, 1],
    'armor': [1, 0, 0, 2, 3],
    'crit_rate': [1, 0, 0, 3, 1],
    'crit_damage': [1, 0, 0, 3, 3],
    'armor_penetration': [1, 0, 0, 4, 1]
}

STAT_FUNCTIONS = {
    'health': lambda x: int(x),
    'ammo': lambda x: int(x),
    'ration': lambda x: int(x),
    'damage': lambda x: int(x),
    'evasion': lambda x: int(x),
    'accuracy': lambda x: int(x),
    'rate_of_fire': lambda x: int(x),
    'move_speed': lambda x: int(x),
    'armor': lambda x: process_armor(x),
    'crit_rate': lambda x: int(x.replace('%', '')),
    'crit_damage': lambda x: int(x.replace('%', '')),
    'armor_penetration': lambda x: int(x)
}


def process_armor(x):
    if isinstance(x.text, str) and x.text.strip():
        return int(x.text)
    else:
        return int(x[0][0][0][-1].text)


def get_profile_table(root):
    """
    Grabs the profile table of the T-Doll.
    :type root: lxml.html.HtmlElement
    :rtype: lxml.html.HtmlElement
    """
    return root.cssselect('.floatright.profiletable')[0][0]


def get_pt_value(pt, lookup):
    """
    Gets a specific value from a profile table.
    :type pt: lxml.html.HtmlElement
    :type lookup: str
    :rtype: str
    """
    exceptions = (IndexError, TypeError, AttributeError)
    for row in pt:
        try:
            row_key = row[0].text.strip().lower()
        except exceptions:
            row_key = None
        if row_key is not None:
            if row_key == lookup.lower():
                try:
                    row_val = row[1].text_content().strip()
                except exceptions:
                    row_val = None
                return row_val


class TDoll(object):
    __slots__ = ('raw', 'id', 'url', 'name', 'origin', 'stats')

    def __init__(self, data=None):
        """
        :type data: dict
        """
        self.raw = data or {}
        self.id = self.raw.get('id')
        self.url = self.raw.get('url')
        self.name = TDollName(self.raw.get('name'))
        self.origin = TDollOrigin(self.raw.get('origin'))
        self.stats = TDollStats(self.raw.get('stats'))

    @staticmethod
    async def short_get(url):
        """
        Shortcut method for getting a webpage's text.
        :type url: str
        :rtype: str
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                page = await data.text()
        return page

    async def from_url(self, url):
        """
        Parses the T-Doll's information from the wiki URL.
        :type url: str
        """
        self.url = url
        doll_html = await self.short_get(url)
        doll_root = lx.fromstring(doll_html)
        self.id = doll_root.cssselect('.indexnumber')[0].text.strip()
        try:
            self.id = int(self.id)
        except (ValueError, TypeError):
            pass
        self.name.from_root(doll_root)
        self.origin.from_root(doll_root)
        self.stats.from_root(doll_root)
        print(self.to_dict())

    def to_dict(self):
        """
        Converts the data wrapper to a dict.
        :rtype: dict
        """
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name.to_dict(),
            'origin': self.origin.to_dict(),
            'stats': self.stats.to_dict()
        }


class TDollName(object):
    __slots__ = ('raw', 'short', 'full')

    def __init__(self, data=None):
        self.raw = data or {}
        self.short = self.raw.get('short')
        self.full = self.raw.get('full')

    def __str__(self):
        return self.short

    def from_root(self, root):
        self.short = root.cssselect('.dollname')[0].text.strip()
        pt = get_profile_table(root)
        self.full = get_pt_value(pt, 'Full name')

    def to_dict(self):
        """
        Converts the data wrapper to a dict.
        :rtype: dict
        """
        return {
            'short': self.short,
            'full': self.full
        }


class TDollOrigin(object):
    __slots__ = ('raw', 'country', 'manufacturer')

    def __init__(self, data=None):
        self.raw = data or {}
        self.country = self.raw.get('country')
        self.manufacturer = self.raw.get('manufacturer')

    def from_root(self, root):
        pt = get_profile_table(root)
        self.country = get_pt_value(pt, 'Country of origin')
        self.manufacturer = get_pt_value(pt, 'Manufacturer')

    def to_dict(self):
        """
        Converts the data wrapper to a dict.
        :rtype: dict
        """
        return {
            'country': self.country,
            'manufacturer': self.manufacturer
        }


class TDollStats(object):
    __slots__ = (
        'raw', 'health', 'ammo', 'ration',
        'damage', 'evasion', 'accuracy', 'rate_of_fire',
        'move_speed', 'armor', 'crit_rate', 'crit_damage',
        'armor_penetration'
    )

    def __init__(self, data=None):
        self.raw = data if data is not None else {}
        for slot in self.__slots__[1:]:
            setattr(self, slot, self.raw.get(slot, 0))

    @staticmethod
    def get_stat_value(tabber, coords, stat):
        curr_elem = tabber
        for coord in coords:
            curr_elem = curr_elem[coord]
        calc = STAT_FUNCTIONS.get(stat)
        return calc(curr_elem.text) if stat != 'armor' else calc(curr_elem)

    def from_root(self, root):
        try:
            gtabb = root.cssselect('.tabbertab')[0][1][0]
        except IndexError:
            gtabb = root.cssselect('.stattabcontainer')[0][0][0]
        for stat in STAT_LOCATIONS:
            stat_value = self.get_stat_value(gtabb, STAT_LOCATIONS.get(stat), stat)
            setattr(self, stat, stat_value)

    def to_dict(self):
        """
        Converts the data wrapper to a dict.
        :rtype: dict
        """
        data = {}
        for slot in self.__slots__[1:]:
            data.update({slot: getattr(self, slot)})
        return data
