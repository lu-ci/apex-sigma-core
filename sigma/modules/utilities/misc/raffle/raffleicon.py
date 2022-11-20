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


def get_matching_emote(guild, emote):
    """
    Gets a matching emote from the given guild.
    :type guild: discord.Guild
    :type emote: str
    :rtype: discord.Emoji
    """
    emote_name = emote.split(':')[1]
    matching_emote = None
    for emote in guild.emojis:
        if emote.name == emote_name:
            matching_emote = emote
    return matching_emote


async def raffleicon(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_guild:
        if pld.args:
            invalid = False
            raffle_icon = pld.args[0]
            disable = raffle_icon.lower() == 'disable'
            if not disable:
                if len(raffle_icon) == 1:
                    try:
                        await pld.msg.add_reaction(raffle_icon)
                    except discord.HTTPException:
                        invalid = True
                else:
                    emote = get_matching_emote(pld.msg.guild, raffle_icon)
                    if emote:
                        try:
                            await pld.msg.add_reaction(emote)
                        except discord.HTTPException:
                            invalid = True
                    else:
                        invalid = True
                if not invalid:
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'raffle_icon', raffle_icon)
                    response = GenericResponse('Raffle icon set.').ok()
                else:
                    response = GenericResponse('Given emote was invalid.').error()
            else:
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'raffle_icon', None)
                response = GenericResponse('Raffle icon disabled.').ok()
        else:
            response = GenericResponse('No emote given.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
