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

import cachetools
import discord


class PaginatorInstance(object):
    def __init__(self, message: discord.Message, items: list, span: int):
        self.message = message
        self.items = items
        self.span = span
        self.current_page = 1

    def get_items(self, get_all: bool = False):
        if get_all:
            return self.items
        else:
            items = PaginatorCore.paginate(self.items, self.current_page, self.span)[0]
        return items

    async def next_page(self):
        self.current_page = PaginatorCore.paginate(self.items, self.current_page + 1, self.span)[1]

    async def prev_page(self):
        self.current_page = PaginatorCore.paginate(self.items, self.current_page - 1, self.span)[1]


class PaginatorCore(object):
    def __init__(self):
        self.paginators = cachetools.TTLCache(500, 300)

    @staticmethod
    def paginate(items: list, pg_num: str or int, span=10):
        try:
            page = abs(int(pg_num))
        except (ValueError, TypeError):
            page = 1
        pages, length = len(items) // span, len(items)
        max_page = pages if length % span == 0 and length != 0 else pages + 1
        page = max_page if page > max_page != 0 else page if page else 1
        start_range, end_range = (page - 1) * span, page * span
        return items[start_range:end_range], page

    def get_paginator(self, mid: int):
        self.paginators.get(mid)

    def add_paginator(self, mid: int, paginator: PaginatorInstance):
        self.paginators.update({mid: paginator})

    def del_paginator(self, mid: int):
        if mid in self.paginators.keys():
            self.paginators.pop(mid)
