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
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.minigames.quiz.mech.utils import scramble as scrfn


async def scramble(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        words = ' '.join(pld.args)
        full = False
        if pld.args[-1].lower() == '--full':
            words = ' '.join(pld.args[:-1])
            full = True
        response = discord.Embed(color=0x3B88C3, title='🔣 Text Scrambler')
        response.description = scrfn(words, full)
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
