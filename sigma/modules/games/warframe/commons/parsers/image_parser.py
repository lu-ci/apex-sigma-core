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

import aiohttp
from lxml import html


class FailedIconGrab(Exception):
    def __init__(self):
        self.message = 'Failed to grab an image due to a key or index error.'


def remove_revision(url):
    dot_split = url.split('.')
    pre_ext = '.'.join(dot_split[:-1])
    post_ext = dot_split[-1]
    ext = post_ext.split('/')[0]
    out_url = f'{pre_ext}.{ext}'
    return out_url


def clean_generics(name):
    sections = name.split('_')
    sects_low = [x.lower() for x in sections]
    if 'vauban' in sects_low:
        name = 'Vauban'
    elif sects_low[-1] == 'blueprint':
        name = '_'.join(sections[:-1])
    return name


async def grab_image(name):
    try:
        name = clean_generics(name)
        page_url = f'http://warframe.wikia.com/wiki/{name}'
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url) as item_page_call:
                item_html = await item_page_call.text()
        item_page = html.fromstring(item_html)
        img_element = item_page.cssselect('.pi-image-thumbnail')[0]
        img_url = remove_revision(img_element.attrib.get('src'))
    except (IndexError, KeyError):
        raise FailedIconGrab
    return img_url
