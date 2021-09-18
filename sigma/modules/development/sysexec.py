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

import subprocess


def from_output(output):
    """
    :type output: bytes
    :rtype: str
    """
    return "" if len(output) <= 1 else f"```\n{output.decode('utf-8')}\n```"


async def sysexec(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    response = None
    if pld.args:
        try:
            process = subprocess.run(pld.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            await pld.msg.add_reaction('✔')
            response = from_output(process.stdout)
        except (OSError, subprocess.SubprocessError) as e:
            cmd.log.error(e)
            await pld.msg.add_reaction('❗')
    else:
        response = 'No input.'
    if response:
        await pld.msg.channel.send(response)
