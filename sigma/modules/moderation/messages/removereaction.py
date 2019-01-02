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
from sigma.core.utilities.generic_responses import permission_denied
from sigma.modules.utilities.misc.other.quote import message_search


async def remove_emote(message: discord.Message, emote: str):
    emote_to_remove = None
    for reaction in message.reactions:
        if isinstance(reaction.emoji, str):
            name = reaction.emoji
        else:
            name = reaction.emoji.name
        if name.lower() == emote.lower():
            emote_to_remove = name
            async for emoji_author in reaction.users():
                await message.remove_reaction(reaction.emoji, emoji_author)
            break
    return emote_to_remove


async def removereaction(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        if len(pld.args) == 2:
            mid, emote = pld.args
            if mid.isdigit():
                message = await message_search(mid, pld.msg)
                if message:
                    if pld.msg.guild.me.permissions_in(message.channel).manage_messages:
                        removed = await remove_emote(message, emote)
                        if removed:
                            response = discord.Embed(color=0x66CC66, title='✅ Reaction removed.')
                        else:
                            response = discord.Embed(color=0x696969, title='🔍 Emote not found on that message.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ I can\'t remove reactions in that channel.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 Message not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid message ID.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = permission_denied('Manage Messages')
    await pld.msg.channel.send(embed=response)
