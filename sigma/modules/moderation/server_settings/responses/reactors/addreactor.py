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

from sigma.core.utilities.generic_responses import denied, error, ok


async def addreactor(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if len(pld.args) >= 2:
            trigger = ' '.join(pld.args[:-1]).lower()
            if len(trigger) <= 200:
                if '.' not in trigger:
                    reaction = pld.args[-1].replace('<', '').replace('>', '')
                    auto_reactions = pld.settings.get('reactor_triggers', {})
                    res_text = 'updated' if trigger in auto_reactions else 'added'
                    auto_reactions.update({trigger.strip(): reaction.strip()})
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'reactor_triggers', auto_reactions)
                    response = ok(f'{trigger} has been {res_text}')
                else:
                    response = error('The trigger can\'t have a dot in it.')
            else:
                response = error('The trigger has a limit of 200 characters.')
        else:
            response = error('Invalid number of arguments.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)
