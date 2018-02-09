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

import discord

from sigma.core.mechanics.command import SigmaCommand


async def wftag(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        if args:
            if len(args) > 1:
                alert_tag = args[0].lower()
                alert_role_search = ' '.join(args[1:]).lower()
                alert_role = None
                for role in message.guild.roles:
                    if role.name.lower() == alert_role_search:
                        alert_role = role
                        break
                if alert_role:
                    wf_tags = await cmd.db.get_guild_settings(message.guild.id, 'WarframeTags')
                    if wf_tags is None:
                        wf_tags = {}
                    if alert_tag not in wf_tags:
                        response_title = f'`{alert_tag.upper()}` has been bound to {alert_role.name}'
                    else:
                        response_title = f'`{alert_tag.upper()}` has been updated to bind to {alert_role.name}'
                    wf_tags.update({alert_tag: alert_role.id})
                    await cmd.db.set_guild_settings(message.guild.id, 'WarframeTags', wf_tags)
                    response = discord.Embed(title=f'✅ {response_title}', color=0x66CC66)
                else:
                    response = discord.Embed(title=f'❗ {alert_role_search.upper()} Was Not Found', color=0xBE1931)
            else:
                response = discord.Embed(title='❗ Not Enough Arguments', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing Was Inputted', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Roles needed.', color=0xBE1931)
    await message.channel.send(embed=response)
