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
from sigma.core.utilities.data_processing import convert_to_seconds


class TestDataProcessing(object):
    @staticmethod
    def test_convert_to_seconds():
        targets = [
            ['00:0:00000001', 1], ['11:10:99', 40299], ['51:99:10', 189550],
            ['711:74', 42734], ['15:88', 988], ['9:59', 599],
            ['51', 51], ['13', 13], ['98', 98],
            ['banana', None], ['1:1:1:1', None], ['-19:x:chinchilla', None]
        ]
        for to_conv, conv_tar in targets:
            try:
                end = convert_to_seconds(to_conv)
            except LookupError:
                end = None
            assert end == conv_tar
