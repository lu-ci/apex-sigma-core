# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import arrow
import discord


async def statistics(cmd, message, args):
    sigma_image = 'https://i.imgur.com/mGyqMe1.png'
    sigma_title = 'Apex Sigma: Statistics'
    support_url = 'https://discordapp.com/invite/aEUCHwX'
    role_count = 0
    for guild in cmd.bot.guilds:
        role_count += len(guild.roles)
    time_dif = arrow.utcnow().timestamp - cmd.bot.start_time.timestamp
    command_rate = str(cmd.bot.command_count / time_dif)[:5]
    message_rate = str(cmd.bot.message_count / time_dif)[:5]
    pop_text = f'Servers: **{len(cmd.bot.guilds)}**'
    pop_text += f'\nChannels: **{len(list(cmd.bot.get_all_channels()))}**'
    pop_text += f'\nRoles: **{role_count}**'
    pop_text += f'\nMembers: **{len(list(cmd.bot.get_all_members()))}**'
    exec_text = f'Commands: **{cmd.bot.command_count}**'
    exec_text += f'\nCommand Rate: **{command_rate}/s**'
    exec_text += f'\nMessages: **{cmd.bot.message_count}**'
    exec_text += f'\nMessage Rate: **{message_rate}/s**'
    response = discord.Embed(color=0x1B6F5F, timestamp=cmd.bot.start_time.datetime)
    response.set_author(name=sigma_title, icon_url=sigma_image, url=support_url)
    response.add_field(name='Population', value=pop_text)
    response.add_field(name='Usage', value=exec_text)
    response.set_footer(text=f'Tracking since {cmd.bot.start_time.humanize()}')
    await message.channel.send(embed=response)
