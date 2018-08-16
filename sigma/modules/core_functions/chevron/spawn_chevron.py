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
    'love', 'comfort', 'light', 'ease', 'power', 'glory', 'riches'
]

bad_attribs = [
    'hunger', 'famine', 'poverty', 'doom', 'war', 'destruction',
    'anxiety', 'pain', 'sadness', 'solitude', 'envy', 'death',
    'blood', 'anguish', 'anger', 'greed', 'gore', 'violence'
]


async def spawn_chevron(ev: SigmaEvent, message: discord.Message):
    if message.guild:
        active = message.channel.id in (await ev.db.get_guild_settings(message.guild.id, 'chevron_channels') or [])
        if active:
            pfx = await ev.db.get_prefix(message)
            if not message.content.startswith(pfx):
                gld_cd = await ev.bot.cool_down.on_cooldown(ev.name, message.guild)
                ath_cd = await ev.bot.cool_down.on_cooldown(ev.name, message.author)
                if not gld_cd and not ath_cd:
                    chev_spwn = False
                    chev_good = None
                    chevron = None
                    color = None
                    chev_roll = secrets.randbelow(100)
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
                    else:
                        await ev.bot.cool_down.set_cooldown(ev.name, message.author, 10)
                    if chev_spwn:
                        await ev.bot.cool_down.set_cooldown(ev.name, message.guild, 60)
                        attrib = secrets.choice(good_attribs) if chev_good else secrets.choice(bad_attribs)
                        response = discord.Embed(color=color, title=f'{chevron} The chevron of {attrib} has spawned.')
                        response.description = f'To catch the chevron type **{pfx}grab {attrib}**.'
                        response.description += f' To destroy the chevron type **{pfx}crush {attrib}**.'
                        response.description += f' Grab good, positive chevrons, and crush bad, negative chevrons.'
                        chev_cache.set_cache(message.channel.id, (chev_good, attrib))
                        await message.channel.send(embed=response)

