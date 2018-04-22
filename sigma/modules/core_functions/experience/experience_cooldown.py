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


import arrow

cd_storage = {}


def is_on_xp_cooldown(user_id: int):
    user_stamp = cd_storage.get(user_id) or 0
    curr_stamp = arrow.utcnow().timestamp
    if user_stamp + 80 < curr_stamp:
        cd_storage.update({user_id: curr_stamp})
        on_cd = False
    else:
        on_cd = True
    return on_cd
