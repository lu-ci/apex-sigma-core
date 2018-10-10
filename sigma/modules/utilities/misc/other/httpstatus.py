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


async def httpstatus(cmd: SigmaCommand, message: discord.Message, args: list):
    lookup = args[0] if args else None
    if lookup:
        status_data = await cmd.db[cmd.db.db_nam].HTTPStatusData.find_one({'code': lookup})
        if status_data:
            status_id = status_data.get('code')
            status_message = status_data.get('message')
            status_description = status_data.get('description')
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name=f'🌐 {status_id}: {status_message}', value=f'{status_description}.')
            bonus = {'cat': 'https://http.cat/images', 'dog': 'https://httpstatusdogs.com/img'}
            bonus_arg = args[-1].lower()
            if bonus_arg in bonus.keys():
                bonus_img = f'{bonus.get(bonus_arg)}/{lookup}.jpg'
                response.set_image(url=bonus_img)
        else:
            response = discord.Embed(color=0x696969, title='🔍 Response code not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
