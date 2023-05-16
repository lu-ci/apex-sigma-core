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

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse


def make_binding_data(roles):
    """
    :type roles: list
    :rtype: dict
    """
    icon_list_base = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🍍 🍅 🍆 🌶 🌽 🍠 🍞 🍗 🍟 🍕 🍺 🍷 🍬 🍙'.split()
    binding_data = {}
    for role in roles:
        role_icon = icon_list_base.pop(secrets.randbelow(len(icon_list_base)))
        binding_data.update({role_icon: role.id})
    return binding_data


async def make_binding_message(bind_data, guild, group_id, description):
    """
    :type bind_data: dict
    :type guild: discord.Guild
    :type group_id: str
    :type description: bool
    :rtype: discord.Embed
    """
    emote_block_lines = []
    for icon_key in bind_data.keys():
        role = guild.get_role(bind_data.get(icon_key))
        binding_line = f'{icon_key} - {role.name}'
        emote_block_lines.append(binding_line)
    emote_block = ' '.join(emote_block_lines)
    toggler_description = 'Press the emote icon under this message corresponding to the role that you want to toggle.'
    guild_icon = str(guild.icon.url) if guild.icon.url else None
    toggler = discord.Embed(color=await get_image_colors(guild_icon))
    toggler.set_author(name=f'Group {group_id} Emote Role Toggles', icon_url=guild_icon)
    if description:
        toggler.description = toggler_description
    toggler.add_field(name='Emote Legend', value=emote_block)
    return toggler


async def fill_toggler_emotes(toggler, emotes):
    """
    :type toggler: discord.Message
    :type emotes: list
    """
    for emote in emotes:
        await toggler.add_reaction(emote)


async def makeemotetoggles(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            group_id = pld.args[0].lower()
            has_desc = False if pld.args[-1].lower() == 'nodesc' else True
            target_ch = pld.msg.channel_mentions[0] if pld.msg.channel_mentions else pld.msg.channel
            emote_groups = pld.settings.get('emote_role_groups') or {}
            if group_id in emote_groups:
                role_items = []
                group_roles = emote_groups.get(group_id)
                if group_roles:
                    for group_role in group_roles:
                        role_item = pld.msg.guild.get_role(group_role)
                        if role_item:
                            role_items.append(role_item)
                        else:
                            group_roles.remove(group_role)
                    emote_groups.update({group_id: group_roles})
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'emote_role_groups', emote_groups)
                    binding_data = make_binding_data(role_items)
                    toggler_response = await make_binding_message(binding_data, pld.msg.guild, group_id, has_desc)
                    toggler_message = await target_ch.send(embed=toggler_response)
                    await fill_toggler_emotes(toggler_message, list(binding_data.keys()))
                    guild_togglers = pld.settings.get('emote_role_togglers') or {}
                    guild_togglers.update({str(toggler_message.id): binding_data})
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'emote_role_togglers', guild_togglers)
                    response = GenericResponse(f'Toggler {group_id} created in {target_ch.name}.').ok()
                else:
                    response = GenericResponse('No groups in the Emote group!').not_found()
            else:
                response = GenericResponse(f'Group {group_id} not found.').not_found()
        else:
            response = GenericResponse('Missing group ID.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)
