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

from sigma.core.utilities.data_processing import convert_to_seconds, get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse


async def createinvite(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.create_instant_invite:
        target = pld.msg.channel_mentions[0] if pld.msg.channel_mentions else pld.msg.channel
        age, uses = 0, 0
        for arg in pld.args:
            if arg.lower().startswith('d:'):
                try:
                    age = convert_to_seconds(arg.partition(':')[-1])
                except (LookupError, ValueError):
                    age = None
            if arg.lower().startswith('u:'):
                try:
                    uses = int(arg.split(':')[-1])
                except ValueError:
                    uses = None
        if age is not None:
            if not age > 86400:
                if uses is not None:
                    if not uses > 100:
                        try:
                            invite = await target.create_invite(max_age=age, max_uses=uses)
                            guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon.url else discord.Embed.Empty
                            response = discord.Embed(color=await get_image_colors(guild_icon))
                            response.set_author(name=f'Invite for {target.name}.', icon_url=guild_icon)
                            age = arrow.get(arrow.utcnow().int_timestamp + age).humanize() if age else None
                            details = f"**Link:** {invite}\n**Expires:** {age or 'Never'}"
                            details += f"\n**Uses:** {uses or 'Unlimited'}"
                            response.description = details
                        except discord.Forbidden:
                            response = GenericResponse('I was unable to make an invite.').error()
                    else:
                        response = GenericResponse('Maximum invite uses is 100.').error()
                else:
                    response = GenericResponse('Max uses must be a number.').error()
            else:
                response = GenericResponse('Maximum invite duration is 24 hours.').error()
        else:
            response = GenericResponse('Please use the format HH:MM:SS.').error()
    else:
        response = GenericResponse('Access Denied. Create Instant Invites needed.').denied()
    await pld.msg.channel.send(embed=response)
