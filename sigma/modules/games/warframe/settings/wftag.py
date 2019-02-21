# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok


async def wftag(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_roles:
        if pld.args:
            if len(pld.args) > 1:
                alert_tag = pld.args[0].lower()
                alert_role_search = ' '.join(pld.args[1:]).lower()
                if alert_role_search == 'disable':
                    wf_tags = pld.settings.get('warframe_tags')
                    if alert_tag in wf_tags:
                        wf_tags.pop(alert_tag)
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'warframe_tags', wf_tags)
                        response = ok('Tag unbound.')
                    else:
                        response = error(f'Nothing is bound to {alert_tag}.')
                else:
                    alert_role = None
                    for role in pld.msg.guild.roles:
                        if role.name.lower() == alert_role_search:
                            alert_role = role
                            break
                    if alert_role:
                        wf_tags = pld.settings.get('warframe_tags')
                        if wf_tags is None:
                            wf_tags = {}
                        if alert_tag not in wf_tags:
                            response_title = f'`{alert_tag.upper()}` has been bound to {alert_role.name}'
                        else:
                            response_title = f'`{alert_tag.upper()}` has been updated to bind to {alert_role.name}'
                        wf_tags.update({alert_tag: alert_role.id})
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'warframe_tags', wf_tags)
                        response = ok(f'{response_title}')
                    else:
                        response = not_found(f'{alert_role_search} not found.')
            else:
                response = error('Not enough arguments.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Roles needed.')
    await pld.msg.channel.send(embed=response)
