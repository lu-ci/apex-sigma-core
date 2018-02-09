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

from sigma.core.mechanics.command import SigmaCommand


async def listwarnings(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_messages:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
    else:
        target = message.author
    if target:
        lookup = {'guild': message.guild.id, 'target.id': target.id, 'warning.active': True}
        warnings = await cmd.db[cmd.db.db_cfg.database].Warnings.find(lookup).to_list(None)
        if warnings:
            warn_list = []
            for warning in warnings:
                warn_id = warning.get('warning').get('id')
                mod_id = warning.get('moderator').get('id')
                moderator = discord.utils.find(lambda x: x.id == mod_id, cmd.bot.get_all_members())
                if moderator:
                    moderator = moderator.name
                else:
                    moderator = warning.get('moderator').get('name')
                warn_time = arrow.get(warning.get('warning').get('timestamp')).format('DD. MMM. YYYY. HH:mm')
                warn_list.append(f'`{warn_id}` by **{moderator}** on {warn_time}.')
            warn_list = '\n'.join(warn_list)
            ending = 'warnings' if len(warnings) > 1 else 'warning'
            start = f'{target.name} has' if target.id != message.author.id else 'You have'
            response = discord.Embed(color=0xFFCC4D)
            response.add_field(name=f'⚠ {start} {len(warnings)} active {ending}.', value=warn_list)
        else:
            start = f'{target.name} doesn\'t' if target.id != message.author.id else 'You don\'t'
            response = discord.Embed(color=0x55acee, title=f'💠 {start} have any warnings.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ You didn\'t tag any user.')
    await message.channel.send(embed=response)
