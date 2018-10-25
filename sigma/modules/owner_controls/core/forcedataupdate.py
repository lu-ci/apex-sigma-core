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


async def forcedataupdate(cmd: SigmaCommand, pld: CommandPayload):
    response = discord.Embed(color=0xF9F9F9, title='⚗ Reinitializing static content...')
    load_status = await message.channel.send(embed=response)
    ready_events = cmd.bot.modules.events.get('dbinit')
    for ready_event in ready_events:
        await ready_event.execute(True)
    response = discord.Embed(color=0x77B255, title=f'✅ Database static content reinitialized.')
    await load_status.edit(embed=response)
