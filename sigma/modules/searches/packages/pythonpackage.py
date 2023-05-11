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

import json

import arrow
import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget

pypi_io_icon = 'https://i.imgur.com/BSUf5p2.png'


async def pythonpackage(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        lookup = '_'.join(pld.args)
        package_url = f'https://pypi.org/pypi/{lookup}/json'
        try:
            package_data = await aioget(package_url, True)
        except json.JSONDecodeError:
            package_data = None
        if package_data:
            cdat = package_data.get('info')
            versions = {}
            if package_data.get('releases'):
                versions = filter(lambda v: v[1], versions.items())
                versions = sorted(versions, key=lambda x: arrow.get(x[1][0].get('upload_time')).int_timestamp)
            if versions:
                created_at = arrow.get(versions[0][1][0].get('upload_time'))
                updated_at = arrow.get(versions[-1][1][0].get('upload_time'))
                package_page = cdat.get('package_url')
                package_title = f'{cdat.get("name")} {versions[-1][0]}'
                response = discord.Embed(color=0x3476a9, timestamp=updated_at.datetime)
                response.description = f'Author: {cdat.get("author") or "Unknown"}'
                response.description += f'\nCreated: {created_at.format("DD. MMM. YYYY")}'
                response.description += f'\n**{cdat.get("summary") or "No summary provided."}**'
                response.set_author(name=package_title, icon_url=pypi_io_icon, url=package_page)
                if cdat.get('keywords'):
                    response.set_footer(text=f'Keywords: {", ".join(cdat.get("keywords").split())}')
                else:
                    response.set_footer(text='Last updated')
            else:
                response = GenericResponse('Package has no versions available.').not_found()
        else:
            response = GenericResponse('Package not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
