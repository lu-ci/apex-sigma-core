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

import asyncio

import aiohttp
import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


async def get_emote_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


async def addemote(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    react_msg = None
    if pld.msg.author.guild_permissions.manage_emojis:
        if not Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
            Ongoing.set_ongoing(cmd.name, pld.msg.guild.id)
            react_embed = discord.Embed(color=0xF9F9F9, title='💬 React with the desired emote.')
            react_msg = await pld.msg.channel.send(embed=react_embed)

            def check_emote(reac, usr):
                same_author = usr.id == pld.msg.author.id
                same_message = reac.message.id == react_msg.id
                return same_author and same_message

            try:
                ae, _au = await cmd.bot.wait_for('reaction_add', timeout=30, check=check_emote)
                working_embed = discord.Embed(title='⬇️ Downloading file...', color=0x3B88C3)
                try:
                    await react_msg.edit(embed=working_embed)
                except discord.NotFound:
                    await pld.msg.channel.send(embed=working_embed)

                react_msg = await pld.msg.channel.fetch_message(react_msg.id)
                emote_to_add = None
                for reaction in react_msg.reactions:
                    if str(reaction.emoji) == str(ae):
                        emote_to_add = reaction.emoji
                        break
                if not isinstance(emote_to_add, str):
                    if pld.args and len(pld.args[0]) > 1:
                        name = pld.args[0]
                    else:
                        # noinspection PyUnresolvedReferences
                        name = emote_to_add.name

                    # noinspection PyUnresolvedReferences
                    image = await get_emote_image(str(emote_to_add.url))
                    try:
                        emote = await pld.msg.guild.create_custom_emoji(name=name, image=image)
                        response = GenericResponse(f'Added emote {emote.name}.').ok()
                    except discord.errors.HTTPException:
                        response = GenericResponse('File size cannot exceed 256kb.').error()
                else:
                    response = GenericResponse('Must be a custom emote.').error()
            except asyncio.TimeoutError:
                response = discord.Embed(color=0x696969, title='🕙 The message timed out.')

            if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
                Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
        else:
            response = GenericResponse('There is already one ongoing.').error()
    else:
        response = GenericResponse('Access Denied. Manage Emotes needed.').denied()
    if react_msg:
        try:
            await react_msg.edit(embed=response)
        except discord.NotFound:
            await pld.msg.channel.send(embed=response)
    else:
        await pld.msg.channel.send(embed=response)
