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

import cachetools


class PaginatorInstance(object):
    """
    The paginator instance handles data display and processing.
    """

    __slots__ = ("message", "items", "span", "current_page")

    def __init__(self, message, items, span):
        """
        :type message: discord.Message
        :type items: list
        :type span: int
        """
        self.message = message
        self.items = items
        self.span = span
        self.current_page = 1

    def get_items(self, get_all=False):
        """
        Grabs the items for the given page
        or all items if they get_all parameter is true.
        :type get_all: bool
        :rtype: list
        """
        if get_all:
            return self.items
        else:
            items = PaginatorCore.paginate(self.items, self.current_page, self.span)[0]
        return items

    async def next_page(self):
        """
        Increases the current page by 1.
        """
        self.current_page = PaginatorCore.paginate(self.items, self.current_page + 1, self.span)[1]

    async def prev_page(self):
        """
        Decreases the current page by 1.
        """
        self.current_page = PaginatorCore.paginate(self.items, self.current_page - 1, self.span)[1]


class PaginatorCore(object):
    """
    The core in charge of tracking and caching paginators.
    """

    __slots__ = ("paginators",)

    def __init__(self):
        self.paginators = cachetools.TTLCache(500, 300)

    @staticmethod
    def paginate(items, pg_num, span=10):
        """
        PAginates a simple list of items.
        :type items: list
        :type pg_num: str or int
        :type span: int
        :rtype: (list, int)
        """
        try:
            page = abs(int(pg_num))
        except (ValueError, TypeError):
            page = 1
        pages, length = len(items) // span, len(items)
        max_page = pages if length % span == 0 and length != 0 else pages + 1
        page = max_page if page > max_page != 0 else page if page else 1
        start_range, end_range = (page - 1) * span, page * span
        return items[start_range:end_range], page

    def get_paginator(self, mid):
        """
        Gets an existing paginator instance.
        :type mid: int
        :rtype: sigma.core.mechanics.paginator.PaginatorInstance
        """
        return self.paginators.get(mid)

    def add_paginator(self, mid, paginator):
        """
        Adds a new paginator instance.
        :type mid: int
        :type paginator: sigma.core.mechanics.paginator.PaginatorInstance
        """
        self.paginators.update({mid: paginator})

    def del_paginator(self, mid):
        """
        Deletes an existing paginator instance.
        :type mid: int
        """
        if mid in self.paginators.keys():
            self.paginators.pop(mid)
