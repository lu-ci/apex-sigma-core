# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import os
import aiml
from sigma.core.mechanics.event import SigmaEvent


chatter_core = aiml.Kernel()


async def chatter_core_init(ev: SigmaEvent):
    chatter_core.verbose(False)
    aiml_files = sorted(os.listdir(ev.resource('aiml_files')))
    for aiml_file in aiml_files:
        chatter_core.learn(ev.resource(f'aiml_files/{aiml_file}'))
