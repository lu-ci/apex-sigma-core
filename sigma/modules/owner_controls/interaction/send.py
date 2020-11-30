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

import discord

from sigma.core.utilities.generic_responses import error, ok, not_found


async def send(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        error_response = error('Bad input.')
        try:
            mode, identifier = pld.args[0].split(':')
            identifier = int(identifier)
        except ValueError:
            await pld.msg.channel.send(embed=error_response)
            return
        mode = mode.lower()
        text = ' '.join(pld.args[1:])
        if mode == 'u':
            target = await cmd.bot.get_user(identifier)
            if not target:
                await pld.msg.channel.send(embed=not_found('User not found.'))
                return
            title_end = f'{target.name}#{target.discriminator}'
        elif mode == 'c':
            target = await cmd.bot.get_channel(identifier)
            if not target:
                await pld.msg.channel.send(embed=not_found('Channel not found.'))
                return
            title_end = f'#{target.name} on {target.guild.name}'
        else:
            await pld.msg.channel.send(embed=error_response)
            return
        if text:
            try:
                await target.send(text)
                response = ok(f'Message sent to {title_end}.')
            except (discord.Forbidden, discord.HTTPException):
                response = error('I can\'t message that user.')
        else:
            response = error('Missing message to send.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
