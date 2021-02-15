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

from sigma.core.utilities.generic_responses import GenericResponse


def make_bar(completed, total):
    """
    :type completed: int
    :type total: int
    :rtype: str
    """
    try:
        fill = int((completed / total) * 10)
    except ZeroDivisionError:
        fill = 0
    empty = 10 - fill
    percentage = int(completed / total * 100)
    bar = f'[{fill * "▣"}{empty * "▢"}] {percentage}%'
    return f'```css\n{bar}\n```'


async def forcedataupdate(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    db_init_events = cmd.bot.modules.events.get('dbinit')
    working_embed = discord.Embed(color=0xF9F9F9, title='⚗ Reinitializing static content...')
    working_embed.description = make_bar(0, len(db_init_events))
    working_msg = await pld.msg.channel.send(embed=working_embed)
    for i, db_init_event in enumerate(db_init_events):
        # noinspection PyBroadException
        try:
            working_embed.description = make_bar(i, len(db_init_events))
            try:
                await working_msg.edit(embed=working_embed)
            except discord.NotFound:
                await pld.msg.channel.send(embed=working_embed)
            await db_init_event.execute(True)
        except Exception:
            cmd.log.error(f'Failed reinitializing {db_init_event.name} content.')
    response = GenericResponse('Database static content reinitialized.').ok()
    try:
        await working_msg.edit(embed=response)
    except discord.NotFound:
        await pld.msg.channel.send(embed=response)
