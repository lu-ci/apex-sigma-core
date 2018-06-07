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


def paginate(items: list, pg_num: str or int, span=10):
    page = 1
    if str(pg_num).isdigit() or str(pg_num)[1:].isdigit():
        page = abs(int(pg_num)) or 1
    start_range = (page - 1) * span
    end_range = page * span
    return items[start_range:end_range], page
