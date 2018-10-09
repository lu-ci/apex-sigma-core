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

import discord

from sigma.core.mechanics.command import SigmaCommand


async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    n = [
        await cmd.db.set_profile(uid, 'sabotaged', True) for uid in [
            478922543764471808, 478922931515424788, 478935902735958017, 478936638312022016, 478937238030516262,
            478940034808938509, 478941241858326539, 478953204223311872, 478954607654076416, 478958121264349185,
            478960760412962837, 478962410414407708, 478966226412896256, 478968942074003473, 478979974494420993,
            478982641845141504, 478983815499350038, 478985072481927190, 478986979380559872, 478992859542978571,
            478996695255089152, 478998737620828161, 479000629277229078, 479002017298382855, 479003703978885121,
            479004945283153932, 479006400266371073, 479007907757686794, 479009450766630932, 479011004634890263,
            479027888562110475, 479030098742214666, 479031638538321922, 479033246571560990, 479034302357831681,
            479035471935045635, 479037088600162306, 479037943747444737, 479039387842248704, 479040996127277068,
            479042289067491340, 479043955800014861, 479048586773135361, 479050222555889675, 479051354334167042,
            479052556815958017, 479054592966000642, 479055681412923403, 479096304501522432, 436527245981515806
        ]
    ][0]
    await message.channel.send('All good.')
