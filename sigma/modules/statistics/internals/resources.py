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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import get_image_colors, user_avatar


async def resources(cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    target = message.mentions[0] if message.mentions else message.author
    reses = ['currency', 'metal', 'biomass', 'sumarum', 'ammunition']
    response = discord.Embed(color=await get_image_colors(user_avatar(target)))
    response.set_author(name=f'{target.name}\'s Resources', icon_url=user_avatar(target))
    boop_head = ['Name', 'Current', 'Local', 'Total']
    boop_data = []
    mixed = 0
    for res in list(sorted(reses)):
        resd = await cmd.db.get_resource(target.id, res)
        mixed += resd.current
        resd_guild = resd.origins.guilds.get(message.guild.id)
        boop_data.append([res.title(), resd.current, resd_guild, resd.total])
    stat_line = f'{target.name} has a total of {mixed} resources over {len(reses)} resource types.'
    response.add_field(name='Resource Stats', value=stat_line)
    response.add_field(name='Resource Listing', value=f'```hs\n{boop(boop_data, boop_head)}\n```', inline=False)
    await message.channel.send(embed=response)
