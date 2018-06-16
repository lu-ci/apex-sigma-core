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
from sigma.core.mechanics.statistics.external.common import StatsConstructor


async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    esh = StatsConstructor()
    cdat = esh.construct_data(cmd, message, args)
    print(cdat)
