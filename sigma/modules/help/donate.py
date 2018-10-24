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


async def donate(cmd: SigmaCommand, message: discord.Message, _args: list):
    sigma_title = 'Sigma Donation Information'
    donation_url = f'{cmd.bot.cfg.pref.website}/donate'
    response = discord.Embed(color=0x1B6F5F, title=sigma_title)
    response.description = f'Care to help out? Come [support]({donation_url}) Sigma!'
    await message.channel.send(embed=response)
