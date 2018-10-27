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
from sigma.core.utilities.data_processing import get_image_colors


async def oserverbots(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        lookup = ' '.join(args)
        try:
            gld = cmd.bot.get_guild(int(lookup))
        except ValueError:
            gld = discord.utils.find(lambda u: u.name.lower() == lookup.lower(), cmd.bot.guilds)
        if gld:
            online_bots, offline_bots = [], []
            total_bots = len([u for u in gld.members if u.bot])
            for user in gld.members:
                if user.bot:
                    name = f'{user.name}#{user.discriminator}'
                    offline_bots.append(name) if str(user.status) == 'offline' else online_bots.append(name)
            if total_bots == 0:
                response = discord.Embed(color=0xBE1931, title='❗ No bots were found on that server.')
            else:
                response = discord.Embed(color=await get_image_colors(gld.icon_url))
                response.set_author(name=f'Bots on {gld.name}', icon_url=gld.icon_url)
                response.add_field(name='Online', value='\n- ' + '\n- '.join(sorted(online_bots)))
                response.add_field(name='Offline', value='\n- ' + '\n- '.join(sorted(offline_bots) or ['None']))
        else:
            response = discord.Embed(color=0x696969, title='🔍 Guild not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
