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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def coinflip(_cmd: SigmaCommand, pld: CommandPayload):
    coin_images = {'heads': 'https://i.imgur.com/qLPkn7k.png', 'tails': 'https://i.imgur.com/Xx5dY4M.png'}
    result = secrets.choice(list(coin_images.keys()))
    response = discord.Embed(color=0x1B6F5F)
    if pld.args:
        choice = pld.args[0].lower()
        if choice.startswith('t') or choice.startswith('h'):
            if choice.lower().startswith('t'):
                choice = 'tails'
            else:
                choice = 'heads'
            out = '☑ Nice guess!' if result == choice.lower() else '🇽 Better luck next time!'
            response = discord.Embed(color=0x1B6F5F, title=out)
    response.set_image(url=coin_images.get(result))
    await pld.msg.channel.send(embed=response)
