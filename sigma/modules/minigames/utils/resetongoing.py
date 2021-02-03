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
from sigma.modules.minigames.utils.ongoing.ongoing import ongoing_storage


async def resetongoing(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
        await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, 300)
        for identifier in [pld.msg.author.id, pld.msg.channel.id, pld.msg.guild.id]:
            for key in ongoing_storage:
                ongoing_list = ongoing_storage.get(key) or []
                if identifier in ongoing_list:
                    ongoing_list.remove(identifier)
                ongoing_storage.update({key: ongoing_list})
        response = GenericResponse('Ongoing user, channel and guild locks cleared.').ok()
    else:
        timeout = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You can clear ongoing markers again in {timeout} seconds.')
    await pld.msg.channel.send(embed=response)
