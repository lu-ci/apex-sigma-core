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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok


async def logmodule(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            module_name = pld.args[0].lower()
            if module_name in cmd.bot.modules.categories:
                logged_modules = pld.settings.get('logged_modules') or []
                if module_name in logged_modules:
                    result = 'disabled'
                    logged_modules.remove(module_name)
                else:
                    result = 'enabled'
                    logged_modules.append(module_name)
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'logged_modules', logged_modules)
                response = ok(f'{module_name.upper()} logging {result}.')
            else:
                response = not_found('Module not found.')
        else:
            response = error('No module given.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
