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

from sigma.modules.games.warframe.commons.parsers.invasion_parser import item_name_fixer


def parse_sales_data(text: str, discount_only: bool = True):
    text = text.strip()
    sale_items = []
    for line in text.split('\n'):
        line = line.split('|')
        name = item_name_fixer(line[0])
        redu = int(line[1])
        plat = int(line[2])
        actv = int(line[4])
        expr = int(line[5])
        if 'prime access' not in name.lower():
            if not discount_only or redu > 0:
                data = {
                    'name':      name,
                    'discount':  redu,
                    'platinum':  plat,
                    'activates': actv,
                    'expires':   expr
                }
                sale_items.append(data)
    return sale_items
