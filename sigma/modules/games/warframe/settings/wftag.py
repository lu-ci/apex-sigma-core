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
from sigma.core.utilities.generic_responses import permission_denied


async def wftag(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        if args:
            if len(args) > 1:
                alert_tag = args[0].lower()
                alert_role_search = ' '.join(args[1:]).lower()
                if alert_role_search == 'disable':
                    wf_tags = await cmd.db.get_guild_settings(message.guild.id, 'WarframeTags')
                    if alert_tag in wf_tags:
                        wf_tags.pop(alert_tag)
                        await cmd.db.set_guild_settings(message.guild.id, 'WarframeTags', wf_tags)
                        response = discord.Embed(color=0x66CC66, title=f'✅ Tag unbound.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing is bound to {alert_tag}.')
                else:
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
                        response = discord.Embed(color=0x66CC66, title=f'✅ {response_title}')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 {alert_role_search} not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Roles')
    await message.channel.send(embed=response)
