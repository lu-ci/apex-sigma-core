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

import secrets

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse


def make_sugg_embed(msg, args, token):
    """
    :type msg: discord.Message
    :type args: list[str]
    :type token: str
    :rtype: discord.Embed
    """
    guild_icon = str(msg.guild.icon.url) if msg.guild.icon.url else None
    sugg_embed = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
    sugg_embed.description = " ".join(args)
    author_name = f'{msg.author.name} [{msg.author.id}]'
    footer_content = f'[{token}]'
    sugg_embed.set_author(name=author_name, icon_url=user_avatar(msg.author))
    sugg_embed.set_footer(icon_url=guild_icon, text=footer_content)
    return sugg_embed


async def serversuggestion(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    sugg_channel = await cmd.db.get_guild_settings(pld.msg.guild.id, 'suggestion_channel')
    if pld.args:
        if sugg_channel:
            channel = pld.msg.guild.get_channel(int(sugg_channel))
            if channel:
                sugg_token = secrets.token_hex(4)
                sugg_msg = await channel.send(embed=make_sugg_embed(pld.msg, pld.args, sugg_token))
                [await sugg_msg.add_reaction(r) for r in ['⬆', '⬇']]
                response = GenericResponse(f'Suggestion {sugg_token} submitted.').ok()
            else:
                response = GenericResponse('Cannot find suggestion channel.').error()
        else:
            response = GenericResponse('Suggestion channel not set.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
