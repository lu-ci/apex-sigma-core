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

import secrets
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.caching import Cacher


chev_cache = Cacher()

good_attribs = [
    'serenity', 'glee', 'joy', 'peace', 'prosperity', 'freedom',
    'elegance', 'fun', 'peanut butter', 'pizza', 'relaxation',
    'love', 'comfort', 'ligh', 'ease', 'power', 'glory', 'riches'
]

bad_attribs = [
    'hunger', 'famine', 'poverty', 'doom', 'war', 'descrution',
    'anxiety', 'pain', 'sadness', 'solitude', 'envy', 'death',
    'blood', 'anguish', 'anger', 'greed', 'gore', 'violence'
]


async def spawn_chevron(ev: SigmaEvent, msg: discord.Message):
    if msg.guild:
        active = await ev.db.get_guild_settings(msg.guild.id, 'spawn_chevrons')
        if active:
            if not await ev.bot.cool_down.on_cooldown(ev.name, msg.guild):
                chev_spwn = False
                chev_good = None
                chevron = None
                color = None
                chev_roll = secrets.randbelow(500)
                if chev_roll <= 3:
                    chev_spwn = True
                    chev_good = True
                    chevron = '🔷'
                    color = 0x55acee
                elif chev_roll == 5:
                    chev_spwn = True
                    chev_good = False
                    chevron = '🔻'
                    color = 0xe75a70
                if chev_spwn:
                    await ev.bot.cool_down.set_cooldown(ev.name, msg.guild, 60)
                    pfx = await ev.db.get_prefix(msg)
                    attrib = secrets.choice(good_attribs) if chev_good else secrets.choice(bad_attribs)
                    response = discord.Embed(color=color, title=f'{chevron} The chevron of {attrib} has spawned.')
                    response.description = f'To catch the chevron type **{pfx}grab {attrib}**.'
                    response.description += ' Red chevrons are bad and will half your current amount.'
                    chev_cache.set_cache(msg.channel.id, (chev_good, attrib))

