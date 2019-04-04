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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found
from sigma.core.utilities.url_processing import aioget

crates_io_icon = 'https://i.imgur.com/Nyw7kSc.png'


async def crates(_cmd: SigmaCommand, pld: CommandPayload):
    lookup = '_'.join(pld.args) if pld.args else None
    if lookup:
        crate_url = f'https://crates.io/api/v1/crates/{lookup}'
        crate_data = await aioget(crate_url, True)
        errors = crate_data.get('errors')
        if not errors:
            owner_data = await aioget(f'{crate_url}/owners', True)
            owners = [f'[{own.get("login")}]({own.get("url")})' for own in owner_data.get('users')]
            cdat = crate_data.get('crate')
            lver = crate_data.get('versions')[0]
            created_at = arrow.get(cdat.get('created_at'))
            updated_at = arrow.get(lver.get('updated_at'))
            crate_page = f'https://crates.io/crates/{cdat.get("id")}'
            crate_title = f'{cdat.get("name")} {cdat.get("max_version")}'
            own_end = 's' if len(owners) != 1 else ''
            response = discord.Embed(color=0x3A6436, timestamp=updated_at.datetime)
            response.description = f'Owner{own_end}: {", ".join(owners)}'
            response.description += f'\nCreated: {created_at.format("DD. MMM. YYYY")}'
            response.description += f'\nDownloads: {cdat.get("downloads")}'
            response.description += f'\n**{cdat.get("description")}**'
            response.set_author(name=crate_title, icon_url=crates_io_icon, url=crate_page)
            if owner_data.get('users'):
                response.set_thumbnail(url=owner_data.get('users')[0].get('avatar'))
            if cdat.get('keywords'):
                response.set_footer(text=f'Keywords: {", ".join(cdat.get("keywords"))}')
            else:
                response.set_footer(text='Last updated')
        else:
            error_details = errors[0].get('detail')
            if error_details == 'Not Found':
                response = not_found('Crate not found.')
            else:
                error_list = [err.get('detail') for err in errors]
                response = errors(f'Crate Error: {". ".join(error_list)}.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)
