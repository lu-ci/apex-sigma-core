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

from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.data_processing import convert_to_seconds

skill_types_by_color = {
    'gold': 'Support',
    'deepskyblue': 'Defense',
    'pink': 'Offense'
}

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


class ShipStats(object):
    """
    Azur lane ship statistics data wrapper.
    """
    __slots__ = (
        'raw', 'firepower', 'health', 'anti_air', 'reload',
        'evasion', 'aviation', 'torpedo', 'oil_consumption',
        'speed', 'luck', 'accuracy', 'anti_submarine', 'armor'
    )

    def __init__(self, data=None):
        """
        :param data: Ship statistics data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.firepower = self.raw.get('firepower', 0)
        self.health = self.raw.get('health', 0)
        self.anti_air = self.raw.get('anti_air', 0)
        self.evasion = self.raw.get('evasion', 0)
        self.aviation = self.raw.get('aviation', 0)
        self.torpedo = self.raw.get('torpedo', 0)
        self.oil_consumption = self.raw.get('oil_consumption', 0)
        self.speed = self.raw.get('speed', 0)
        self.luck = self.raw.get('luck', 0)
        self.accuracy = self.raw.get('accuracy', 0)
        self.anti_submarine = self.raw.get('anti_submarine', 0)
        self.armor = self.raw.get('armor') or None
        self.reload = self.raw.get('reload', 0)

    @property
    def average(self):
        """
        Returns the average value of all ship stats.
        :return:
        :rtype: float
        """
        stat_attrs = [
            'firepower', 'health', 'anti_air', 'reload',
            'evasion', 'aviation', 'torpedo', 'oil_consumption',
            'speed', 'luck', 'accuracy', 'anti_submarine'
        ]
        return round(sum([getattr(self, satt) for satt in stat_attrs]) / len(stat_attrs), 2)

    def from_tabber(self, tabber):
        """
        Parses a single tabber instance to get stats from.
        :param tabber: A tabbed table element.
        :type tabber: lxml.html.objectify.Element
        :return:
        :rtype:
        """
        table = tabber[1][0]
        stat_coords = {
            'health': [0, 1], 'armor': [0, 3], 'reload': [0, 5], 'speed': [0, 7],
            'firepower': [1, 1], 'torpedo': [1, 3], 'evasion': [1, 5], 'luck': [1, 7],
            'anti_air': [2, 1], 'aviation': [2, 3], 'oil_consumption': [2, 5], 'accuracy': [2, 7],
            'anti_submarine': [3, 1]

        }
        for stat_coord_key in stat_coords:
            stat_coord_row, stat_coord_col = stat_coords.get(stat_coord_key)
            stat_val = table[stat_coord_row][stat_coord_col].text
            stat_val = 0 if not stat_val or not stat_val.isdigit() else stat_val.strip()
            try:
                stat_val = int(stat_val)
            except ValueError:
                pass
            setattr(self, stat_coord_key, stat_val)

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'firepower': self.firepower,
            'health': self.health,
            'anti_air': self.anti_air,
            'reload': self.reload,
            'evasion': self.evasion,
            'aviation': self.aviation,
            'torpedo': self.torpedo,
            'oil_consumption': self.oil_consumption,
            'speed': self.speed,
            'luck': self.luck,
            'accuracy': self.accuracy,
            'anti_submarine': self.anti_submarine,
            'armor': self.armor
        }


class ShipStatsByRetrofit(object):
    """
    Wraps the statistics based on normal and retrofit mode.
    """
    __slots__ = ('raw', 'normal', 'retrofit')

    def __init__(self, data=None):
        """
        :param data: Ship statistics data by retrofit mode.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.normal = ShipStatsByLevel(self.raw.get('normal'))
        self.retrofit = ShipStatsByLevel(self.raw.get('retrofit'))

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'normal': self.normal.to_dict(),
            'retrofit': self.retrofit.to_dict()
        }


class ShipStatsByLevel(object):
    """
    Wraps the the base, level 100 and 120 statistics.
    """
    __slots__ = ('raw', 'base', 'maxed', 'awake')

    def __init__(self, data=None):
        """
        :param data: Ship statistics data by level.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.base = ShipStats(self.raw.get('base'))
        self.maxed = ShipStats(self.raw.get('maxed'))
        self.awake = ShipStats(self.raw.get('awake'))

    def describe(self, awoken=False):
        """
        Returns a text block meant for embed information.
        :param awoken: Is the function describing a retrofit.
        :type awoken: bool
        :return:
        :rtype: str
        """
        out_proto = [
            ['Health', 'health'],
            ['Armor', 'armor'],
            ['Reload', 'reload'],
            ['Speed', 'speed'],
            ['Firepower', 'firepower'],
            ['Torpedo', 'torpedo'],
            ['Aviation', 'aviation'],
            ['Oil Cost', 'oil_consumption'],
            ['Accuracy', 'accuracy'],
            ['Evasion', 'evasion'],
            ['Luck', 'luck'],
            ['Anti-Air', 'anti_air'],
            ['Anti-Sub', 'anti_submarine']
        ]
        out_list = []
        lvconts = [self.base, self.maxed] if not awoken else [self.maxed, self.awake]
        for proto_data in out_proto:
            out_sub = [proto_data[0]]
            for lvcont in lvconts:
                out_sub.append(str(getattr(lvcont, proto_data[1])))
            out_list.append(out_sub)
        out_list.append(['Average', str(self.base.average), str(self.maxed.average)])
        out = boop(out_list, ['Stat', 'Base', 'Lv. 100'])
        return out

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'base': self.base.to_dict(),
            'maxed': self.maxed.to_dict(),
            'awake': self.awake.to_dict()
        }


class ShipSkin(object):
    """
    Wraps a ship's skin image data.
    """
    __slots__ = ('raw', 'name', 'url')

    def __init__(self, data=None):
        """
        :param data: Ship skin data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.name = self.raw.get('name')
        self.url = self.raw.get('url')

    def from_tabber(self, tabber):
        """
        Parses a single tabber instance to get the skin.
        :param tabber: A tabbed table element.
        :type tabber: lxml.html.objectify.Element
        :return:
        :rtype:
        """
        self.name = tabber.attrib.get('title')
        self.url = tabber[1][0][0].attrib.get('src')
        self.url = self.url.replace('/thumb', '').replace('/W/', '/w/')
        self.url = '/'.join(self.url.split('/')[:-1])
        self.url = f'https://azurlane.koumakan.jp{self.url}'

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'name': self.name,
            'url': self.url
        }


class ShipImages(object):
    """
    Wraps all the images a ship has,
    such as the small and original image, and skin images.
    """
    __slots__ = ('raw', 'small', 'main', 'chibi', 'skins')

    def __init__(self, data=None):
        """
        :param data: Ship image data and lists.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.small = self.raw.get('small')
        self.main = ShipSkin(self.raw.get('main'))
        self.chibi = self.raw.get('chibi')
        self.skins = [ShipSkin(skdat) for skdat in self.raw.get('skins', [])]

    def get_skin(self, lookup):
        """
        Gets a skin based on the lookup query.
        :param lookup: What to search for.
        :type lookup: str
        :return:
        :rtype: sigma.modules.games.azur_lane.models.azur_lane_ship.ShipSkin
        """
        out = None
        for skin in self.skins:
            if skin.name.lower() == lookup.lower():
                out = skin
                break
        if not out:
            for skin in self.skins:
                if lookup.lower() in skin.name.lower():
                    out = skin
                    break
        return out

    def from_etree(self, page):
        """
        Parses the ship's images from an LXML-parsed page.
        :param page: The LXML etree page to parse.
        :type page: lxml.html.objectify.Etree
        :return:
        :rtype:
        """
        url_base = 'https://azurlane.koumakan.jp'
        self.small = page.cssselect('.image')[0][0].attrib.get('src')
        self.small = f'{url_base}{self.small}'
        skin_elements = page.cssselect('.azl_box_body')[0][0]
        for skin_element in skin_elements:
            skin_item = ShipSkin()
            skin_item.from_tabber(skin_element)
            self.skins.append(skin_item)
            if skin_item.name == 'Default':
                self.main = skin_item
        try:
            self.chibi = page.cssselect('#talkingchibi')[0][0].attrib.get('src')
        except IndexError:
            self.chibi = None
        if self.chibi:
            self.chibi = f'{url_base}{self.chibi}'

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'small': self.small,
            'main': self.main.to_dict(),
            'chibi': self.chibi,
            'skins': [skitem.to_dict() for skitem in self.skins]
        }


class ShipLimitBreakContainer(object):
    """
    Holds data that depend on limit breaks.
    """
    __slots__ = ('raw', 'first', 'second', 'third', 'is_skills')

    def __init__(self, data=None, is_skills=False):
        """
        :param data: The limit break data to contain.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.is_skills = is_skills
        if is_skills:
            self.first = ShipSkill(self.raw.get('first'))
            self.second = ShipSkill(self.raw.get('second'))
            self.third = ShipSkill(self.raw.get('thirt'))
        else:
            self.first = self.raw.get('first')
            self.second = self.raw.get('second')
            self.third = self.raw.get('thirt')

    def to_list(self):
        """
        Turns the data in this class into a list.
        :return:
        :rtype: list[ShipSkill]
        """
        return [skill for skill in [self.first, self.second, self.third] if skill.type is not None]

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        if not self.is_skills:
            dict_data = {
                'first': self.first,
                'second': self.second,
                'third': self.third
            }
        else:
            dict_data = {
                'first': self.first.to_dict(),
                'second': self.second.to_dict(),
                'third': self.third.to_dict()
            }
        return dict_data


class ShipEquipment(object):
    """
    Wraps the ship's equipment details.
    """
    __slots__ = ('raw', 'slot', 'efficiency', 'equippable')

    def __init__(self, data=None):
        """
        :param data: The ship equipment data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.slot = self.raw.get('slot')
        self.efficiency = ShipLimitBreakContainer(self.raw.get('efficiency'))
        self.equippable = self.raw.get('equippable')

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'slot': self.slot,
            'efficiency': self.efficiency.to_dict(),
            'equippable': self.equippable
        }


class ShipSkill(object):
    """
    Wraps the ship's skill data.
    """
    __slots__ = ('raw', 'name', 'type', 'description')

    def __init__(self, data=None):
        """
        :param data: The ship skill data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.name = self.raw.get('name')
        self.type = self.raw.get('type')
        self.description = self.raw.get('description')

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'name': self.name,
            'type': self.type,
            'description': self.description
        }


class ShipConstruction(object):
    """
    Wraps data for a ship's contruction details.
    """
    __slots__ = ('raw', 'possible', 'time', 'light', 'heavy', 'special', 'limited', 'exchange')

    def __init__(self, data=None):
        """
        :param data: The ship construction data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.possible = self.raw.get('possible')
        self.time = self.raw.get('time')
        self.light = self.raw.get('light')
        self.heavy = self.raw.get('heavy')
        self.special = self.raw.get('special')
        self.limited = self.raw.get('limited')
        self.exchange = self.raw.get('exchange')

    def from_table(self, table):
        """
        Parses a ship's construction info from a table.
        :param table: A table to parse.
        :type table: lxml.html.objectify.Element
        :return:
        :rtype:
        """
        const_nest = {0: 'light', 1: 'heavy', 2: 'special', 3: 'limited', 4: 'exchange'}
        const_time = table[1][0].text_content().strip()
        try:
            self.time = convert_to_seconds(const_time)
            self.possible = True
        except LookupError:
            self.time = None
            self.possible = False
        for cell_index, cell in enumerate(table[3][:5]):
            cell_key = const_nest.get(cell_index)
            cell_text = cell.text_content().strip()
            if cell_text == '-':
                const_type_possible = False
            else:
                const_type_possible = True
            setattr(self, cell_key, const_type_possible)

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'possible': self.possible,
            'time': self.time,
            'light': self.light,
            'heavy': self.heavy,
            'special': self.special,
            'limited': self.limited,
            'exchange': self.exchange
        }


class ShipDropMission(object):
    """
    WRaps data for where a ship can drop.
    """
    __slots__ = ('raw', 'chapter', 'map', 'possible', 'boss_only')

    def __init__(self, data=None):
        """
        :param data: Data on where the ship can drop.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.chapter = self.raw.get('chapter')
        self.map = self.raw.get('map')
        self.possible = self.raw.get('possible')
        self.boss_only = self.raw.get('boss_only')

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'chapter': self.chapter,
            'map': self.map,
            'possible': self.possible,
            'boss_only': self.boss_only
        }


class ShipAcquisition(object):
    """
    Wraps the ship's methods of acquisition
    """
    __slots__ = ('raw', 'construction', 'missions', 'notes')

    def __init__(self, data=None):
        """
        :param data: The ship acquisition data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.construction = ShipConstruction(self.raw.get('construction'))
        self.missions = [ShipDropMission(sdrm) for sdrm in self.raw.get('missions', [])]
        self.notes = self.raw.get('notes')

    def from_table(self, table):
        """
        Parses a ship's acquisition info from a table.
        :param table: A table to parse.
        :type table: lxml.html.objectify.Element
        :return:
        :rtype:
        """
        self.construction.from_table(table)
        for row_index, row in enumerate(table[1:6]):
            if len(row) in [14, 15, 19]:
                for cell_index, cell in enumerate(row[-13:]):
                    sdm = ShipDropMission()
                    sdm.map = row_index + 1 if row_index != 4 else 'SOS'
                    sdm.chapter = cell_index + 1
                    cell_color = cell.attrib.get('style')
                    if cell_color:
                        cell_color = cell_color.split(':')[-1].lower()
                        if cell_color == 'lemonchiffon':
                            sdm.possible = True
                            sdm.boss_only = True
                        elif cell_color.endswith('green'):
                            sdm.possible = True
                            sdm.boss_only = False
                        else:
                            sdm.possible = False
                            sdm.boss_only = False
                    else:
                        sdm.possible = False
                        sdm.boss_only = False
                    self.missions.append(sdm)
        self.missions = list(sorted(self.missions, key=lambda mshn: str(mshn.map)))
        self.missions = list(sorted(self.missions, key=lambda mshn: mshn.chapter))
        last_row = table[-1]
        if last_row[0].text_content().strip() == 'Additional Notes':
            self.notes = last_row[1].text_content().strip().replace('\n', '. ')

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'construction': self.construction.to_dict(),
            'missions': [smitm.to_dict() for smitm in self.missions],
            'notes': self.raw.get('notes')
        }


class ShipQuote(object):
    """
    Wraps the ship's quotes and voice lines.
    """
    __slots__ = ('raw', 'file', 'event', 'jp', 'en', 'note')

    def __init__(self, data=None):
        """
        :param data: The ship acquisition data.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.file = self.raw.get('file')
        self.event = self.raw.get('event')
        self.jp = self.raw.get('jp')
        self.en = self.raw.get('en')
        self.note = self.raw.get('note')

    def from_row(self, row):
        """
        Parses quote data from a table row.
        :param row: A table row.
        :type row: lxml.html.objectify.Element
        :return:
        :rtype:
        """
        self.file = row[1][0].attrib.get('href') if len(row[1]) else None
        self.event = row[2].text.strip() if row[2].text else None
        self.jp = row[3].text_content().replace('\n', ' ').strip()
        self.jp = self.jp if self.jp else None
        self.en = row[4].text_content().replace('\n', ' ').strip()
        self.en = self.en if self.en else None
        self.note = row[5].text_content().replace('\n', ' ').strip()
        self.note = self.note if self.note else None

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'file': self.file,
            'event': self.event,
            'jp': self.jp,
            'en': self.en,
            'note': self.note
        }


class AzurLaneShip(object):
    """
    Azur lane ship information and statistics wrapper.
    """
    __slots__ = (
        'raw', 'url', 'id', 'name', 'rarity', 'type',
        'subtype', 'faction', 'stats', 'images',
        'equipment', 'skills', 'ranks', 'acquisition', 'quotes',
        'faction_icon', 'faction_short', 'rarity_color'
    )

    def __init__(self, data=None):
        """
        :param data: The entire ship's data document.
        :type data: dict
        """
        self.raw = data if data is not None else {}
        self.id = self.raw.get('id')
        self.url = self.raw.get('url')
        self.name = self.raw.get('name')
        self.rarity = self.raw.get('rarity')
        self.rarity_color = rarity_colors.get(self.rarity.lower()) if self.rarity else 0xf9f9f9
        self.type = self.raw.get('type')
        self.subtype = self.raw.get('subtype')
        self.faction = self.raw.get('faction')
        self.faction_icon = faction_icons.get(self.faction.lower()) if self.faction else None
        self.faction_short = faction_prefixes.get(self.faction.lower()) if self.faction else None
        self.stats = ShipStatsByRetrofit(self.raw.get('stats'))
        self.images = ShipImages(self.raw.get('images'))
        self.equipment = [ShipEquipment(seqdat) for seqdat in self.raw.get('equipment', [])]
        self.skills = ShipLimitBreakContainer(self.raw.get('skills'), True)
        self.ranks = ShipLimitBreakContainer(self.raw.get('ranks'))
        self.acquisition = ShipAcquisition(self.raw.get('acquisition'))
        self.quotes = [ShipQuote(sqdat) for sqdat in self.raw.get('quotes', [])]

    def to_dict(self):
        """
        Turns the data in this class into a dictionary.
        :return:
        :rtype: dict
        """
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'rarity': self.rarity,
            'type': self.type,
            'subtype': self.subtype,
            'faction': self.faction,
            'stats': self.stats.to_dict(),
            'images': self.images.to_dict(),
            'equipment': [eqitm.to_dict() for eqitm in self.equipment],
            'skills': self.skills.to_dict(),
            'ranks': self.ranks.to_dict(),
            'acquisition': self.acquisition.to_dict(),
            'quotes': [qtitm.to_dict() for qtitm in self.quotes]
        }

    def from_tabbers(self, tabbers):
        """
        Parses ship details from a list of tabbed tables.
        :param tabbers: A list of tabbed table elements.
        :type tabbers: list[lxml.html.objectify.Element]
        :return:
        :rtype:
        """
        sub_coords = {
            'Base Stats': self.stats.normal.base,
            'Level 100': self.stats.normal.maxed,
            'Level 120': self.stats.normal.awake,
            'Level 100 Retrofit': self.stats.retrofit.maxed,
            'Level 120 Retrofit': self.stats.retrofit.awake,
        }
        for tabber in tabbers:
            tabber_title = tabber.attrib.get('title').strip() if tabber.attrib.get('title') else None
            if tabber_title in sub_coords:
                sub_coords[tabber_title].from_tabber(tabber)
            elif tabber_title in ['Japanese Ship Lines', 'Japanese Lines Extended']:
                vl_table = tabber[1]
                for vl_row in vl_table[2:]:
                    if len(vl_row) == 6:
                        ship_quote = ShipQuote()
                        ship_quote.from_row(vl_row)
                        self.quotes.append(ship_quote)

    def from_tables(self, tables):
        """
        Parses a ship's detailed information from table entries.
        :param tables: A list of tables to parse.
        :type tables: list[lxml.html.objectify.Element]
        :return:
        :rtype:
        """
        for table in tables:
            table = table[0]
            try:
                table_title = table[0][0].text_content().strip() if table[0][0].text_content() else None
            except IndexError:
                table_title = None
            if table_title == 'Equipment':
                for table_row in table[2:]:
                    eqp_ent = ShipEquipment()
                    eqp_ent.slot = int(table_row[0].text_content())
                    efficiency_pieces = [pce.strip().strip('%') for pce in table_row[1].text_content().split('→')]
                    new_pieces = []
                    for efi_ix, efi_pc in enumerate(efficiency_pieces):
                        try:
                            piece_value = int(efi_pc)
                        except ValueError:
                            if efi_pc == '--':
                                piece_value = efficiency_pieces[efi_ix]
                            else:
                                piece_value = None
                        new_pieces.append(piece_value)
                    efficiency_pieces = new_pieces
                    lbrk_eqp = ShipLimitBreakContainer()
                    if len(efficiency_pieces) == 2:
                        efficiency_pieces = [efficiency_pieces[0], None, efficiency_pieces[-1]]
                    elif len(efficiency_pieces) == 1:
                        efficiency_pieces = [None, None, None]
                    lbrk_eqp.first, lbrk_eqp.second, lbrk_eqp.third = efficiency_pieces
                    eqp_ent.efficiency = lbrk_eqp
                    eqp_ent.equippable = table_row[2][0].text_content().strip()
                    eqp_ent.equippable = eqp_ent.equippable if eqp_ent.equippable else None
                    self.equipment.append(eqp_ent)
            elif table_title == 'Limit Break Ranks':
                self.ranks = ShipLimitBreakContainer()
                self.skills = ShipLimitBreakContainer(is_skills=True)
                lbrk_rnk_list = []
                lbrk_skl_list = []
                for row in table[1:]:
                    upograde_desc = row[1].text_content().strip()
                    if upograde_desc:
                        lbrk_rnk_list.append(upograde_desc)
                    skill_name = row[2].text_content().strip()
                    if skill_name:
                        skill_desc = row[3].text_content().strip()
                        skill_color = row[2].attrib.get('style').split(':')[-1].lower()
                        lbrk_skl_ent = ShipSkill()
                        lbrk_skl_ent.name = skill_name
                        lbrk_skl_ent.description = skill_desc
                        lbrk_skl_ent.type = skill_types_by_color.get(skill_color)
                        lbrk_skl_list.append(lbrk_skl_ent)
                nest_keys = {0: 'first', 1: 'second', 2: 'third'}
                for lbrk_cont in [(self.ranks, lbrk_rnk_list), (self.skills, lbrk_skl_list)]:
                    for lbrk_index in nest_keys:
                        try:
                            lbrk_value = lbrk_cont[1][lbrk_index]
                        except IndexError:
                            lbrk_value = None
                        if lbrk_value:
                            lbrk_key = nest_keys.get(lbrk_index)
                            setattr(lbrk_cont[0], lbrk_key, lbrk_value)
            elif table_title == 'Construction':
                self.acquisition.from_table(table)

    async def save(self, db):
        """
        :param db: The database handler reference.
        :type db: sigma.core.mechanics.database.Database
        :return:
        :rtype:
        """
        al_coll = db[db.db_nam].AzurLaneShips
        exists = bool(await al_coll.find_one({'id': self.id}))
        if not exists:
            await al_coll.insert_one(self.to_dict())
        else:
            await al_coll.update_one({'id': self.id}, {'$set': self.to_dict()})


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
