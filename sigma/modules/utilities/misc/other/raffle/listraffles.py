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
import arrow

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


async def listraffles(cmd: SigmaCommand, message: discord.Message, args: list):
    lookup = {'Author': message.author.id, 'Active': True}
    raffle_docs = await cmd.db[cmd.db.db_cfg.database].Raffles.find(lookup).to_list(None)
    all_channels = list(cmd.bot.get_all_channels())
    if raffle_docs:
        raffle_lines = []
        for raf_doc in raffle_docs:
            raffle_channel = discord.utils.find(lambda c: c.id == raf_doc.get('Channel'), all_channels)
            if raffle_channel:
                location = f'in **#{raffle_channel.name}** on **{raffle_channel.guild.name}**.'
            else:
                location = 'in an unknown location.'
            hum_time = arrow.get(raf_doc.get('End')).humanize()
            raffle_line = f'`{raf_doc.get("ID")}` ends {hum_time} {location}.'
            raffle_lines.append(raffle_line)
        outlist = '\n'.join(raffle_lines)
        response = discord.Embed(color=message.author.color)
        response.set_author(name=f'{message.author.name}\'s Raffles', icon_url=user_avatar(message.author))
        response.description = outlist
    else:
        response = discord.Embed(color=0x696969, title='🔍 You have no pending raffles.')
    await message.channel.send(embed=response)
