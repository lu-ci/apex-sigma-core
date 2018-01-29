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


def make_move_log_embed(log_embed, guild):
    gld = guild
    creation_time = arrow.get(gld.created_at).format('DD. MMMM YYYY')
    bot_count = 0
    user_count = 0
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    guild_text = f'Name: **{gld.name}**'
    guild_text += f'\nOwner: **{gld.owner.name}**#*{gld.owner.discriminator}*'
    guild_text += f'\nID: **{gld.id}**'
    guild_text += f'\nCreated: **{creation_time}**'
    nums_text = f'Members: **{user_count}**'
    nums_text += f'\nBots: **{bot_count}**'
    nums_text += f'\nChannels: **{len(gld.channels)}**'
    nums_text += f'\nRoles: **{len(gld.roles)}**'
    log_embed.add_field(name='Guild Info', value=guild_text)
    log_embed.add_field(name='Guild Stats', value=nums_text)
