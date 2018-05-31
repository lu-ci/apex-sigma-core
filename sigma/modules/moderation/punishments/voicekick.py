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
from sigma.core.utilities.permission_processing import hierarchy_permit


async def voicekick(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).kick_members:
        if message.mentions:
            target = message.mentions[0]
            if cmd.bot.user.id != target.id:
                if message.author.id != target.id:
                    above_hier = hierarchy_permit(message.author, target)
                    is_admin = message.author.permissions_in(message.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(message.guild.me, target)
                        if above_me:
                            if target.voice:
                                tvc = target.voice.channel
                                tempvc = discord.utils.find(lambda x: x.name == 'Kick Hall', message.guild.channels)
                                if not tempvc:
                                    tempvc = await message.guild.create_voice_channel('Kick Hall')
                                await target.move_to(tempvc)
                                await tempvc.delete()
                                remove_title = f'👢 {target.name} has been removed from {tvc.name}.'
                                response = discord.Embed(color=0xc1694f, title=remove_title)
                            else:
                                not_in_voice = f'❗ {target.name} is not in a voice channel.'
                                response = discord.Embed(color=0xBE1931, title=not_in_voice)
                        else:
                            response = discord.Embed(title='⛔ Target is above my highest role.', color=0xBE1931)
                    else:
                        response = discord.Embed(title='⛔ Can\'t kick someone equal or above you.', color=0xBE1931)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You can\'t kick yourself.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t kick myself.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Kick permissions needed.', color=0xBE1931)
    await message.channel.send(embed=response)
