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

from sigma.core.utilities.generic_responses import GenericResponse


async def whisper(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        if pld.msg.guild:
            guild_id = pld.msg.guild.id
        elif pld.args[0].isdigit():
            guild_id = int(pld.args[0])
        else:
            guild_id = None
        if str(guild_id) == pld.args[0]:
            pld.args.pop(0)
        if guild_id:
            whisper_chn_id = await cmd.db.get_guild_settings(guild_id, 'whisper_channel')
            if whisper_chn_id:
                whisper_message = ' '.join(pld.args)
                if whisper_message:
                    whisper_data = {
                        'channel_id': whisper_chn_id,
                        'whisper': whisper_message,
                        'reported': False
                    }
                    await cmd.db.col.Whispers.insert_one(whisper_data)
                    response = GenericResponse('Whisper submitted.').ok()
                else:
                    response = GenericResponse('Missing message to send.').error()
            else:
                response = GenericResponse('Whisper channel not set for that guild.').error()
        else:
            response = GenericResponse('Invalid guild ID.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
