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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.mechanics.resources import SigmaResource


async def wiperesources(cmd: SigmaCommand, pld: CommandPayload):
    try:
        target = await cmd.bot.get_user(int(pld.args[0])) if pld.args else None
    except ValueError:
        target = None
    if target:
        colls = await cmd.db[cmd.db.db_nam].list_collection_names()
        reses = list(sorted([coll[:-8].lower() for coll in colls if coll.endswith('Resource')]))
        for res in reses:
            new_res = SigmaResource({})
            await cmd.db.update_resource(target.id, res, new_res)
        response = discord.Embed(color=0xFFCC4D, title=f'🔥 Ok, I\'ve wiped {target.display_name}\'s resources.')
    else:
        response = discord.Embed(color=0x696969, title='🔍 User not found.')
    await pld.msg.channel.send(embed=response)
