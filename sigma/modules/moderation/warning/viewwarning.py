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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import permission_denied


async def viewwarning(cmd, message, args):
    if message.author.guild_permissions.manage_messages:
        if message.mentions:
            if len(args) == 2:
                target = message.mentions[0]
                warn_id = args[1].lower()
                lookup = {
                    'guild': message.guild.id,
                    'target.id': target.id,
                    'warning.id': warn_id,
                    'warning.active': True
                }
                warn_data = await cmd.db[cmd.db.db_cfg.database].Warnings.find_one(lookup)
                if warn_data:
                    mod_id = warn_data.get('moderator').get('id')
                    author = discord.utils.find(lambda x: x.id == mod_id, cmd.bot.get_all_members())
                    if author:
                        author_descrp = f'{author.mention}\n{author.name}#{author.discriminator}'
                    else:
                        wmod = warn_data.get('moderator')
                        author_descrp = f'<@{wmod.get("id")}>\n{wmod.get("name")}#{wmod.get("discriminator")}'
                    target_avatar = user_avatar(target)
                    target_descrp = f'{target.mention}\n{target.name}#{target.discriminator}'
                    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
                    response.set_author(name=f'Warning {warn_id} information.', icon_url=target_avatar)
                    response.add_field(name='⚠ Warned User', value=target_descrp, inline=True)
                    response.add_field(name='🛡 Moderator', value=author_descrp, inline=True)
                    response.add_field(name='📄 Reason', value=warn_data.get('warning').get('reason'), inline=False)
                    response.set_footer(text=f'[{warn_data.get("warning").get("id")}] UserID: {target.id}')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 {target.name} has no {warn_id} warning.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Both user tag and warning ID are needed.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ You didn\'t tag any user.')
    else:
        response = permission_denied('Manage Messages')
    await message.channel.send(embed=response)
