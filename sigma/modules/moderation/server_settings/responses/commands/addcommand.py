"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, ok
from sigma.modules.utilities.tools.imgur import upload_image


async def addcommand(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            attachment = len(pld.args) == 1 and pld.msg.attachments
            if len(pld.args) >= 2 or attachment:
                trigger = pld.args[0].lower()
                if '.' not in trigger:
                    if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                        if attachment:
                            client_id = cmd.bot.modules.commands['imgur'].cfg.get('client_id')
                            content = await upload_image(pld.msg.attachments[0].url, client_id)
                        else:
                            content = ' '.join(pld.args[1:])
                        if content:
                            custom_commands = pld.settings.get('custom_commands', {})
                            res_text = 'updated' if trigger in custom_commands else 'added'
                            custom_commands.update({trigger: content})
                            await cmd.db.set_guild_settings(pld.msg.guild.id, 'custom_commands', custom_commands)
                            response = ok(f'{trigger} has been {res_text}')
                        else:
                            response = error('Bad image.')
                    else:
                        response = error('Can\'t replace an existing core command.')
                else:
                    response = error('The command can\'t have a dot in it.')
            else:
                response = error('Not enough arguments.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
