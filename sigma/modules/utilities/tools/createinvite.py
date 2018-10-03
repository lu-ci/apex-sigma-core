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

import arrow

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied
from sigma.core.utilities.data_processing import get_image_colors, convert_to_seconds


async def createinvite(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.create_instant_invite:
        target = message.channel_mentions[0] if message.channel_mentions else message.channel
        age, uses = 0, 0
        for arg in args:
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
                            response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
                            response.set_author(name=f'Invite for {target.name}.', icon_url=message.guild.icon_url)
                            age = arrow.get(arrow.utcnow().timestamp + age).humanize() if age else None
                            details = f"**Link:** {invite}\n**Expires:** {age or 'Never'}"
                            details += f"\n**Uses:** {uses or 'Unlimited'}"
                            response.description = details
                        except discord.Forbidden:
                            response = discord.Embed(color=0xBE1931, title='❗ I was unable to make an invite.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Maximum invite uses is 100.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Max uses must be a number.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Maximum invite duration is 24 hours.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
    else:
        response = permission_denied('Create Instant Invites')
    await message.channel.send(embed=response)
